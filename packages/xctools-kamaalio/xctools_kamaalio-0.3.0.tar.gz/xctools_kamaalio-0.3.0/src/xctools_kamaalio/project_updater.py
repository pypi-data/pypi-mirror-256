from pathlib import Path

from kamaaalpy.dicts import omit_empty


class ProjectUpdater:
    project_configuration: Path

    def __init__(self) -> None:
        for path in Path.cwd().glob("**/*"):
            if path.name == "project.pbxproj":
                self.project_configuration = path
                break
        else:
            raise ProjectUpdaterException("No project path found")

    def bump_version(self, build_number: int | None, version_number: str | None):
        has_changes = self.__edit(
            object_to_update=omit_empty(
                {
                    "CURRENT_PROJECT_VERSION": str(build_number),
                    "MARKETING_VERSION": version_number,
                }
            )
        )
        if has_changes:
            print("Applied changes to xcode project")
        else:
            print("No changes where needed")

    def __edit(self, object_to_update: dict[str, str]):
        if object_to_update == {}:
            return False

        project_configuration_file_lines = (
            self.project_configuration.read_text().splitlines()
        )
        keys_to_update = object_to_update.keys()
        has_changes = False
        for line_number, line in enumerate(project_configuration_file_lines):
            for key in keys_to_update:
                if key not in line:
                    continue

                amount_of_tabs = line.count("\t")
                tabs = "\t" * amount_of_tabs
                project_configuration_file_lines[
                    line_number
                ] = f"{tabs}{key} = {object_to_update[key]};"
                has_changes = True
                break

        if not has_changes:
            return False

        if len(project_configuration_file_lines[-1]) != 0:
            project_configuration_file_lines.append("")

        self.project_configuration.write_text(
            "\n".join(project_configuration_file_lines)
        )
        return True


class ProjectUpdaterException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
