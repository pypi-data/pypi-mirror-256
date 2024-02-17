from pathlib import Path
import boto3
import webbrowser
import pkg_resources

import argparse
import subprocess
import os
import sys
import botocore.exceptions
import configparser
import cmd
import logging
from .pipeline.command_handler import handle_command # type: ignore

# from commands.config_command import handle_config_pipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Set logging level for botocore to ERROR to suppress stack traces
logging.getLogger("botocore").setLevel(logging.ERROR)


class AWSnapShell(cmd.Cmd):
    prompt = "(awsnap) "

    def do_open(self, profile):
        """
        Open AWS Console with a specific profile.
        Usage:
            open <profile>
        """
        try:
            sso_url = get_sso_url_from_profile(profile)
            open_aws_console(profile, sso_url)
            logging.info(
                f"Successfully opened AWS console for profile {profile}"
            )  # noqa
        except Exception as e:
            logging.error(
                f"Failed to open AWS console for profile {profile}: {str(e)}"
            )  # noqa

    def do_login(self, profile):
        """
        Authenticate with AWS SSO.
        Usage:
            login <profile>
        """
        authenticate_sso(profile)

    def do_list(self, args):
        """
        List available AWS profiles.
        Usage:
            just type 'list'
        """
        list_profiles()

    def do_exit(self, args):
        """
        Exit the interactive shell...
        Usage:
            just type 'exit'
        """
        return True

    def do_pipeline(self, args):
        """
        WIP – Manage AWSnap pipelines.
        Usage:
            pipeline <subcommand> <args>
        """
        handle_command(args)

    def default(self, args):
        print(f"Unknown command: {args} (type 'help' for available commands)")


def list_profiles():
    config_path = Path.home() / ".aws" / "config"
    config = configparser.ConfigParser()
    config.read(config_path)

    profiles = [
        section.replace("profile ", "")
        for section in config.sections()
        if section.startswith("profile ")
    ]

    print("Available Profiles:")
    for profile in profiles:
        print(f"  - {profile}")


def open_aws_console(profile, sso_url):
    sso_url, region = get_sso_url_from_profile(profile)
    try:
        # Create the session with the region if available
        session = (
            boto3.Session(profile_name=profile, region_name=region)
            if region
            else boto3.Session(profile_name=profile)
        )

        if not sso_credentials_exist(session):
            authenticate_sso(profile)
            if not sso_credentials_exist(session):
                raise Exception("SSO authentication failed")

        webbrowser.open(sso_url)
        logging.info(f"Opened AWS console for profile {profile}")

    except Exception as err:
        logging.error(
            f"Failed to open AWS console for profile {profile}: {str(err)}"
        )  # noqa
        raise


def sso_credentials_exist(session):
    try:
        session.client("sts").get_caller_identity()
        return True
    except (
        botocore.exceptions.BotoCoreError,
        botocore.exceptions.ClientError,
    ):
        return False


def authenticate_sso(profile):
    try:
        command = [
            "aws",
            "sso",
            "login",
            "--profile",
            profile,
        ]
        subprocess.run(command, check=True)

        logging.info(f"Successfully authenticated SSO for profile {profile}")
        return True
    except subprocess.CalledProcessError as err:
        logging.error(
            f"An error occurred during SSO authentication for profile {profile}: {err}"  # noqa
        )
        return False
    except Exception as err:
        logging.error(
            f"An error occurred during SSO authentication for profile {profile}: {err}"  # noqa
        )
        return False


def get_sso_url_from_profile(profile):
    config = configparser.ConfigParser()
    config.read(f"{os.path.expanduser('~')}/.aws/config")

    sso_session = config.get(f"profile {profile}", "sso_session")
    sso_start_url = config.get(f"sso-session {sso_session}", "sso_start_url")
    region = config.get(
        f"profile {profile}", "region", fallback=None
    )  # Fetching the region

    return sso_start_url, region


def export_temporary_aws_credentials(profile):
    try:
        session = boto3.Session(profile_name=profile)
        credentials = session.get_credentials()
        access_key = credentials.access_key
        secret_key = credentials.secret_key
        session_token = credentials.token

        credentials_path = Path.home() / ".aws" / "credentials"
        config = configparser.ConfigParser()

        # Read existing credentials if they exist
        if credentials_path.exists():
            config.read(credentials_path)

        if "default" not in config.sections():
            config.add_section("default")

        config.set("default", "aws_access_key_id", access_key)
        config.set("default", "aws_secret_access_key", secret_key)
        config.set("default", "aws_session_token", session_token)

        with open(credentials_path, "w") as f:
            config.write(f)

        logging.info(
            "Temporary AWS credentials have been written to the default profile in ~/.aws/credentials"  # noqa
        )
        return True  # Ensure to return True after successful execution
    except Exception as err:
        logging.error(f"Failed to export temporary AWS credentials: {err}")
        return False


def run_shell_command(profile, command):
    export_temporary_aws_credentials(profile)
    print(f"Running command for profile {profile}: {command}")
    os.system(command)


def get_version():
    # Replace 'your_package_name' with the actual name of your package as specified in the 'pyproject.toml' file.
    package_name = 'awsnap'

    try:
        # Get the distribution based on the package name and return its version.
        return pkg_resources.get_distribution(package_name).version
    except pkg_resources.DistributionNotFound:
        # Handle the case where the distribution could not be found
        return "unknown"



def main():
    parser = argparse.ArgumentParser(
        description="AWSnap: An AWS Utility to help manage your projects and sso sessions.",
    )
    parser.add_argument("-p", "--profile", help="AWS profile name")
    parser.add_argument(
        "--open", action="store_true", help="Open AWS console"
    )  # noqa
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Enter interactive mode",
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List available profiles",
    )
    parser.add_argument(
        "command",
        nargs="*",
        help="Command followed by its arguments to run in the shell",
    )
    # add a version flag to check the version of the tool
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {get_version()}",
    )
    # parser.add_argument(
    #     "--pipeline",
    #     help="Manage AWSnap pipelines",
    #     action="store_true",
    # )

    args = parser.parse_args()

    if args.interactive:
        AWSnapShell().cmdloop()
    elif args.command:
        shell_command = " ".join(args.command)
        run_shell_command(args.profile, shell_command)
    elif args.list:
        list_profiles()
    elif args.open:  # Open console when --open flag is used
        sso_url, _ = get_sso_url_from_profile(args.profile)
        open_aws_console(args.profile, sso_url)
    # elif args.pipeline:
        # handle_command(args.pipeline)
    elif args.profile:  # Export credentials when --profile flag is used
        session = boto3.Session(profile_name=args.profile)

        if not sso_credentials_exist(session):
            logging.info("SSO credentials expired. Initiating SSO login.")
            if not authenticate_sso(args.profile):
                print(
                    "Failed to authenticate with SSO. Please check your credentials and try again."  # noqa
                )
                sys.exit(1)

        if not export_temporary_aws_credentials(args.profile):
            print("Failed to export temporary AWS credentials.")
            sys.exit(1)
    else:
        parser.print_help()
