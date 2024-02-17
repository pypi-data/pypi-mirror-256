import yaml, json, time, logging, subprocess

logger = logging.getLogger(__name__)

def msg(cmd, out, err):
    message = out + '\n' + err
    return ' '.join(cmd) + ": " + message.strip()

class CommandError(Exception):
    def __init__(self, cmd, result):
        super().__init__(msg(cmd, result.stdout.strip(), result.stderr.strip()))

class KubectlError(Exception):
    def __init__(self, cmd, out, err):
        super().__init__(msg(cmd, out, err))

class HelmError(Exception):
    def __init__(self, cmd, out, err):
        super().__init__(msg(cmd, out, err))

class Command:
    def run(self, cmd, host = None, exceptionOnFail = False):
        _cmd = cmd.split() if isinstance(cmd, str) else cmd
        if not host:
            cmd = _cmd
        elif host['type'] == 'deployment':
            name = f"deployment/{host['name']}"
            cmd = ["kubectl", "exec", name, "--namespace", host['namespace'], '--']
            cmd.extend(_cmd)
        elif host['type'] == 'pod':
            cmd = ["kubectl", "exec", host['name'], "--namespace", host['namespace'], '--']
            cmd.extend(_cmd)
        else:
            raise Exception(f"Unsupport host type: {host['type']}")
        logger.info(f"{' '.join(cmd)}: start...")
        if "|" in cmd:
            _cmd = ' '.join(cmd)
            result = subprocess.run(_cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines = True, shell = True)
        else:
            result = subprocess.run(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines = True)
        if result.returncode != 0:
            if exceptionOnFail:
                raise CommandError(cmd, result)
            logger.info(f"{' '.join(cmd)}: return {result.returncode}.")
        else:
            logger.info(f"{' '.join(cmd)}: succeed.")
        logger.debug(f"{msg(cmd, result.stdout.strip(), result.stderr.strip())}.")
        return result.returncode, result.stdout.strip(), result.stderr.strip()

    def runs(self, cmds, host = None, exceptionOnFail = False):
        for cmd in cmds:
            if self.run(cmd, host, exceptionOnFail)[0] != 0:
                return False
        return True

class Kubectl(Command):
    def serialize_labels(self, labels):
        selectors = []
        for k, v in labels.items():
            if isinstance(v, list):
                selectors.append(f"{k} in ({','.join(v)})")
            elif isinstance(v, str):
                selectors.append(f"{k}={v}")
            else:
                raise Exception(f"Unkown Label Structure {labels}")
        return ','.join(selectors)

    def wait_for_beacon(self, beacon, wait_for):
        cmd = ['kubectl', 'wait', beacon.get('target', 'pod'), f"--for={wait_for}"]
        if 'namespace' in beacon:
            cmd.extend(['--namespace', beacon['namespace']])
        else:
            cmd.append('-A')
        if 'labels' in beacon:
            label_selector = self.serialize_labels(beacon['labels'])
            cmd.extend(['-l', label_selector])
        cmd.extend(['--timeout', beacon.get('timeout', '5m')])
        code, out, err = self.run(cmd)
        if code != 0:
            if wait_for == 'delete' and "the server doesn't have a resource type" in err:
                logger.info(f"The CRD of {beacon['target']} Not Found.")
                return
            raise KubectlError(cmd, out, err)

    def wait_for_readiness(self, beacon):
        self.wait_for_beacon(beacon, 'condition=Ready')

    def wait_for_deletion(self, beacon):
        self.wait_for_beacon(beacon, 'delete')

    def wait_for_desire(self, beacon):
        timeout = int(beacon.get('timeout', '300'))
        start_time = time.time()
        archived = False
        while time.time() - start_time < timeout:
            cmd = ["kubectl", "get", beacon["name"], "--namespace", beacon['namespace'], '-o', f"jsonpath='{beacon['jsonpath']}'"]
            code, out, err = self.run(cmd)
            if code == 0:
                state = out.strip("'")
                if state == beacon["desire"]:
                    logger.info(f"{' '.join(cmd)}: achieve desired: {state}.")
                    archived = True
                    break
                logger.info(f"{' '.join(cmd)}: Current state: '{state}', continue waiting for desire state {beacon['desire']}...")
            else:
                if "NotFound" in err or "not found" in err:
                    logger.info(f"{' '.join(cmd)}: {beacon['name']} not found yet.")
                else:
                    raise KubectlError(cmd, out, err)
            time.sleep(20)
        if not archived:
            raise Exception(f"Timeout: {' '.join(cmd)}: not achieve desired: {beacon['desire']}.")

    def should_install_or_upgrade(self, yamlFiles):
        yamls = {file: 0 for file in yamlFiles}
        for f in yamls:
            cmd = ["kubectl", "diff", "-f", f]
            code, out, err = self.run(cmd)
            if code == 0:
                logger.info(f"{' '.join(cmd)}: no difference.")
            elif code == 1:
                logger.info(f"{' '.join(cmd)}: Changed.")
                yamls[f] += 1
            else:
                raise KubectlError(cmd, out, err)
        return sum(yamls.values()) > 0

    def install_or_upgrade(self, yamlFiles):
        for f in yamlFiles:
            cmd = ['kubectl', 'apply', '-f', f]
            self.run(cmd, exceptionOnFail = True)

    def uninstall(self, yamlFiles):
        for f in yamlFiles:
            cmd = ['kubectl', 'delete', '-f', f]
            code, out, err = self.run(cmd)
            if code == 0:
                logger.info(f"{' '.join(cmd)}: uninstall successfully.")
                return
            if 'resource mapping not found' in err and 'ensure CRDs are installed first' in err:
                logger.info(f"{' '.join(cmd)}: CRD not found.")
                return
            if 'NotFound' in err:
                logger.info(f"{' '.join(cmd)}: resources not found.")
                return
            raise KubectlError(cmd, out, err)

class Helm(Command):
    def get_chart_metadata(self, chart):
        cmd = ['helm', "show", "chart", chart['ref']]
        if "version" in chart:
            cmd.extend(['--version', chart['version']])
        if "repo" in chart:
            cmd.extend(["--repo", chart["repo"]])
        code, out, err = self.run(cmd)
        if code != 0:
            raise HelmError(cmd, out, err)
        metadata = yaml.safe_load(out)
        logger.debug(f"Chart {chart['ref']} metadata retrieved.")
        return metadata

    def get_current_revision(self, release_name, namespace):
        cmd = ['helm', "status", release_name, "--namespace", namespace, "--output", "json"]
        code, out, err = self.run(cmd)
        if code != 0:
            if "not found" in err:
                logger.debug(f"Release {release_name} not Found.")
                return None
            raise HelmError(cmd, out, err)
        status = json.loads(out)
        revision = {
                "release": {
                    "name": release_name,
                    "namespace": namespace,
                    },
                "revision": status["version"],
                "status": status["info"]["status"],
                "updated": status["info"]["last_deployed"],
                "description": status["info"].get("description"),
                "notes": status["info"].get("notes"),
                }
        logger.debug(f"Current revision of {release_name}: {revision['revision']}")
        return revision

    def get_current_revision_chart_metadata(self, release_name, namespace):
        CHART_METADATA_TEMPLATE = """
name: {{ .Release.Chart.Metadata.Name }}
version: {{ .Release.Chart.Metadata.Version }}
"""
        cmd = ['helm', "get", 'all', release_name, "--namespace", namespace, "--template", '{{ .Release.Chart.Metadata.Name }} {{ .Release.Chart.Metadata.Version }}']
        code, out, err = self.run(cmd)
        if code != 0:
            raise HelmError(cmd, out, err)
        chart_metadata = {"name": out.split()[0], "version": out.split()[1]}
        logger.debug(f"The chart in current revision: {chart_metadata['name']} {chart_metadata['version']}")
        return chart_metadata

    def get_current_revision_values(self, release_name, namespace):
        cmd = ['helm', "get", 'values', release_name, "--namespace", namespace, "--output", "json"]
        code, out, err = self.run(cmd)
        if code != 0:
            raise HelmError(cmd, out, err)
        values = json.loads(out)
        logger.debug(f"The values in current revision: {values}")
        return values

    def should_install_or_upgrade(self, release, chart):
        logger.debug(f"Check Whether Release {release['name']} in namespace {release['namespace']} needs to upgrade.")

        revision = self.get_current_revision(release["name"], release["namespace"])
        if not revision:
            logger.info(f"Release {release['name']} not found")
            return True
        if revision["status"] != "deployed":
            logger.info(f"The Status of Release {release['name']}: {revision['status']}")
            return True

        revision['chart'] = self.get_current_revision_chart_metadata(release["name"], release["namespace"])
        chart['metadata'] = self.get_chart_metadata(chart)
        if revision['chart']['name'] != chart['metadata']['name']:
            logger.info(f"Old Chart: {revision['chart']['name']}, New Chart: {chart['metadata']['name']}")
            return True
        if revision['chart']['version'] != chart['metadata']['version']:
            logger.info(f"Old Version: {revision['chart']['name']}, New Version: {chart['metadata']['version']}")
            return True

        revision["values"] = self.get_current_revision_values(release["name"], release["namespace"])
        if revision["values"] != release["values"]:
            logger.debug(f"Old Values:\n{revision['values']}")
            logger.debug(f"New Values:\n{release['values']}")
            logger.info("Values Changed")
            return True

        logger.debug(f"Release {release['name']} is up to date.")
        return False

    def install_or_upgrade(self, release, chart):
        with open(release["valuesFile"], 'w') as fo:
            yaml.dump(release["values"], fo, default_flow_style=False, sort_keys=False, indent=2)
        cmd = ["helm", "upgrade", "--install", release['name'], chart['ref'], '--values', release['valuesFile'], "--namespace", release['namespace'], "--create-namespace", '--wait', "--atomic", '--timeout', "5m"]
        if 'version' in chart:
            cmd.extend(["--version", chart['version']])
        if 'repo' in chart:
            cmd.extend(['--repo', chart['repo']])
        self.run(cmd, exceptionOnFail = True)
        logger.info(f"Successfully install/upgrade Release {release['name']} of Chart {chart['ref']}.")

    def uninstall(self, release):
        cmd = ['helm', 'uninstall', release['name'], "--namespace", release['namespace'], '--wait', '--timeout', '5m']
        self.run(cmd, exceptionOnFail = True)
        logger.info(f"Successfully uninstall Release {release['name']} in namespace {release['namespace']}.")

command = Command()
helm = Helm()
kubectl = Kubectl()
