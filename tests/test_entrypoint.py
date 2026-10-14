import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class TestEntrypoint(unittest.TestCase):
    def test_template_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            stub = Path(directory) / "kamidana"
            stub.write_text('#!/usr/bin/env bash\nprintf "%s\\n" "$@" > "$KAMIDANA_ARGS_FILE"\n')
            stub.chmod(0o755)
            args_file = Path(directory) / "args"
            env = {key: value for key, value in os.environ.items()
                   if not key.startswith("INPUTS_")}
            env.update({
                "PATH": directory + os.pathsep + os.environ["PATH"],
                "GITHUB_ACTION_PATH": str(ROOT),
                "KAMIDANA_ARGS_FILE": str(args_file),
                "INPUTS_OUTPUT_FILE": str(Path(directory) / "output"),
                "INPUTS_TEE": "false",
                "GITHUB_CONTEXT": "",
                "JOB_CONTEXT": "",
                "RUNNER_CONTEXT": "",
            })

            for template, expected in (
                ("main.j2", "./main.j2"),
                ("testdata/main.j2", "./testdata/main.j2"),
                ("./main.j2", "./main.j2"),
                ("../main.j2", "../main.j2"),
                ("/tmp/main.j2", "/tmp/main.j2"),
                ("C:/templates/main.j2", "C:/templates/main.j2"),
                ("C:\\templates\\main.j2", "C:\\templates\\main.j2"),
                ("a template.j2", "./a template.j2"),
            ):
                for dump_context in ("false", "true"):
                    with self.subTest(template=template, dump_context=dump_context):
                        env["INPUTS_TEMPLATE"] = template
                        env["INPUTS_DUMP_CONTEXT"] = dump_context
                        subprocess.run(
                            [str(ROOT / "entorypoint.sh")],
                            cwd=directory, env=env, check=True, capture_output=True,
                        )
                        self.assertEqual(args_file.read_text().splitlines()[-1], expected)

            env.pop("INPUTS_TEMPLATE")
            env["INPUTS_DUMP_CONTEXT"] = "false"
            subprocess.run(
                [str(ROOT / "entorypoint.sh"), "main.j2", "-d", "data.json"],
                cwd=directory, env=env, check=True, capture_output=True,
            )
            self.assertEqual(args_file.read_text().splitlines()[-3:], [
                "./main.j2", "-d", "data.json",
            ])
