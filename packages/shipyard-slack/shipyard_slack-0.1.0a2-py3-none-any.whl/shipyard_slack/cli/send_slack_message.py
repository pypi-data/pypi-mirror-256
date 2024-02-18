import os
import re
import sys
import time
import glob
import argparse
import urllib.parse

from slack_sdk import WebClient
from zipfile import ZipFile
from shipyard_bp_utils import files as file_utils
from shipyard_bp_utils.args import create_shipyard_link
from shipyard_slack import SlackClient

EXIT_CODE_INCORRECT_PARAM = 200


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--destination-type",
        dest="destination_type",
        default="channel",
        required=True,
        choices={"channel", "dm"},
    )
    parser.add_argument("--channel-name", dest="channel_name", required=False)
    parser.add_argument(
        "--user-lookup-method",
        dest="user_lookup_method",
        default="email",
        choices={"display_name", "real_name", "email"},
        required=False,
    )
    parser.add_argument("--users-to-notify", dest="users_to_notify", required=False)
    parser.add_argument("--message", dest="message", required=True)
    parser.add_argument(
        "--file-upload",
        dest="file_upload",
        default="no",
        required=True,
        choices={"yes", "no"},
    )
    parser.add_argument(
        "--conditional-send",
        dest="conditional_send",
        default="always",
        required=False,
        choices={"file_exists", "file_dne", "always"},
    )
    parser.add_argument(
        "--source-file-name-match-type",
        dest="source_file_name_match_type",
        default="exact_match",
        choices={"exact_match", "regex_match"},
        required=False,
    )
    parser.add_argument("--source-file-name", dest="source_file_name", required=False)
    parser.add_argument(
        "--source-folder-name", dest="source_folder_name", default="", required=False
    )
    parser.add_argument("--slack-token", dest="slack_token", required=True)

    parser.add_argument(
        "--include-file-in-thread",
        dest="include_file_in_thread",
        default="yes",
        required=False,
    )

    args = parser.parse_args()
    if args.destination_type == "channel" and not args.channel_name:
        parser.error("--destination-type channel requires --channel-name")
    elif args.destination_type == "dm" and not args.users_to_notify:
        parser.error("--destination-type dm requires --users-to-notify")

    if args.users_to_notify and not args.user_lookup_method:
        parser.error("--users-to-notify requires a --user-lookup-method")

    if args.file_upload == "yes" and (
            not args.source_file_name_match_type or not args.source_file_name
    ):
        parser.error(
            "--file-upload yes requires --source-file-name and --source-file-name-match-type"
        )

    return args


def get_message_details(message_response):
    """
    Return the channel_id and timestamp from the message_resposne. Used for updating the message
    or responding in a thread to the message.
    """
    channel_id = message_response["channel"]
    timestamp = message_response["ts"]
    return channel_id, timestamp


def create_user_id_list(users_to_notify, user_lookup_method):
    """
    Create a list of all users to be notified.
    """
    users_to_notify = [x.strip() for x in users_to_notify.split(",")]
    # TODO: Add support for looking up users by display name
    user_id_list = []
    for user in users_to_notify:
        if user in ["@here", "@channel", "@everyone"]:
            user_id_list.append(user.replace("@", ""))
        else:
            print("Looking up " + user)
            user_id = slack_user_id_lookup(slack_connection, user, user_lookup_method)
            user_id_list.append(user_id)
    return user_id_list


def create_name_tags(user_id_list):
    """
    Create a string that consists of all the user_id tags
    that will be added at the beginning of a message.
    """
    names_to_prepend = ""

    for user_id in user_id_list:
        if user_id not in ["channel", "here", "everyone"]:
            names_to_prepend += f"<@{user_id}> "
        else:
            names_to_prepend += f"<!{user_id}> "

    return names_to_prepend


def _has_file(message: str) -> bool:
    """Returns true if a message string has the {{file.txt}} pattern

    Args:
        message (str): The message

    Returns:
        bool:
    """
    pattern = r"\{\{[^\{\}]+\}\}"
    res = re.search(pattern, message)
    if res is not None:
        return True
    return False


def _extract_file(message: str) -> str:
    pattern = r"\{\{[^\{\}]+\}\}"
    res = re.search(pattern, message).group()
    file_pattern = re.compile(r"[{}]+")
    text = re.sub(file_pattern, "", res)
    if re.search("^text:", text) is None:
        print("Error: the parameter needs to be prefixed with text:")
        sys.exit(EXIT_CODE_INCORRECT_PARAM)
    split = re.split("^text:", text)  # will be a list of two

    return split[1]


def _read_file(file: str, message: str) -> str:
    try:
        with open(file, "r") as f:
            content = f.read()
            f.close()
    except Exception as e:
        print(
            f"Could not load the contents of file {file}. Make sure the file extension is provided"
        )
        raise (FileNotFoundError)
    pattern = r"\{\{[^\{\}]+\}\}"
    # msg = re.sub(
    #     '\n', '<br>', f"{re.sub(pattern,'',message)} <br><br> {content}")
    msg = f"{re.sub(pattern, '', message)} \n \n {content}"
    return msg


def create_blocks(message, shipyard_link, download_link=""):
    """
    Create blocks for the main message, a divider, and context that links to Shipyard.
    If a download link is provided, creates a button block to immediately start that download.
    For more information: https://api.slack.com/block-kit/building
    """
    # check to see if the message is templated
    if _has_file(message):
        file = _extract_file(message)
        message = _read_file(file, message)

    message_section = {
        "type": "section",
        "text": {"type": "mrkdwn", "text": message, "verbatim": True},
    }
    divider_section = {"type": "divider"}
    context_section = {
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": f"Sent by Shipyard | <{shipyard_link}|Click Here to Edit>",
            }
        ],
    }

    if download_link != "":
        download_section = {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Download File"},
                    "value": "file_download",
                    "url": download_link,
                    "style": "primary",
                }
            ],
        }
        blocks = [message_section, download_section, divider_section, context_section]
    else:
        blocks = [message_section, divider_section, context_section]

    return blocks




def get_file_download_details(file_response):
    """
    Return the download_link from the file_response.
    Used for updating the message with a download button.
    """
    download_link = file_response["file"]["url_private_download"]
    return download_link


def compress_files(file_names):
    """
    Given a list of files, compress all of them into a single file.
    Keeps the existing directory structure in tact.
    """
    archive_file_name = "archive.zip"
    print(f"{len(file_names)} files found. Compressing the files...")
    cwd = os.getcwd()
    with ZipFile(archive_file_name, "w") as zip_file:
        for path in file_names:
            zip_file.write(path, path.replace(cwd, ""))
    print(
        f"All {len(file_names)} files were successfully compressed into {archive_file_name}"
    )
    return archive_file_name


def is_too_large(file_path):
    """
    Determine if the file is too large for Slack's upload limit.
    Used to conditionally compress a file.
    """
    byte_max = 1000000000
    if os.stat(file_path).st_size >= byte_max:
        return True
    else:
        return False


def determine_file_to_upload(
        source_file_name_match_type, source_folder_name, source_file_name
):
    """
    Determine whether the file name being uploaded to Slack
    will be named archive_file_name or will be the source_file_name provided.
    """
    if source_file_name_match_type == "regex_match":
        file_names = find_all_local_file_names(source_folder_name)
        matching_file_names = find_all_file_matches(
            file_names, re.compile(source_file_name)
        )

        file_to_upload = compress_files(matching_file_names)
    else:
        source_full_path = combine_folder_and_file_name(
            folder_name=source_folder_name, file_name=source_file_name
        )
        byte_max = 1000000000

        if is_too_large(source_full_path):
            file_utils.are_files_too_large([source_full_path], byte_max)
            file_utils.compress_files([source_full_path])

            print(f"{source_full_path} is too large. Compressing the file...")
            file_to_upload = compress_files([source_full_path])
        else:
            file_to_upload = source_full_path
    return file_to_upload


def send_slack_message_with_file(
        slack_connection: WebClient,
        message,
        channel,
        shipyard_link,
        file_to_upload,
        include_file_in_thread=True,
):
    """
    Sends an initial Slack message with the file upload status in progress.
    Attempts to upload the file. If successful, updates the first message with a download button.
    If unsuccessful, updates the message to let users know.
    """
    # this is the backwards compatible way to send a message with a file
    if include_file_in_thread:
        message_with_file_status = message + "\n\n _(File is currently uploading...)_"
        message_response = send_slack_message(
            slack_connection,
            message_with_file_status,
            channel,
            create_blocks(message_with_file_status, shipyard_link),
        )
        channel_id, timestamp = get_message_details(message_response)
        file_response = upload_file_to_slack(
            slack_connection,
            file_name=file_to_upload,
            channel_name=channel,
            timestamp=timestamp,
        )
        if file_response:
            download_link = get_file_download_details(file_response)
            update_slack_message(
                slack_connection,
                message,
                channel_id=channel_id,
                blocks=create_blocks(
                    message, download_link=download_link, shipyard_link=shipyard_link
                ),
                timestamp=timestamp,
            )
        else:
            message_with_file_status = (
                    message + "\n\n _(File could not be uploaded. Check log for details)_"
            )
            update_slack_message(
                slack_connection,
                message,
                channel_id=channel_id,
                blocks=create_blocks(
                    message_with_file_status, shipyard_link=shipyard_link
                ),
                timestamp=timestamp,
            )

    # this is the case where we want to send the file in the main part of the message
    else:
        # post initial message
        message_response = slack_connection.chat_postMessage(
            channel=channel, text=message
        )
        if message_response["ok"]:
            upload_response = slack_connection.files_upload(
                channels=channel, file=file_to_upload, filename=file_to_upload
            )
            download_link = get_file_download_details(upload_response)
            if upload_response["ok"]:
                print("Message with file upload posted successfully")
            else:
                print(f"File upload failed: {upload_response['error']}")
        else:
            print(f"Message posting failed: {message_response['error']}")


def should_message_be_sent(
        conditional_send, source_folder_name, source_file_name, source_file_name_match_type
):
    """
    Determine if a slack message should be sent based on the parameters provided.
    """

    source_full_path = combine_folder_and_file_name(
        source_folder_name, source_file_name
    )

    if source_file_name_match_type == "exact_match":
        if (
                (conditional_send == "file_exists" and os.path.exists(source_full_path))
                or (conditional_send == "file_dne" and not os.path.exists(source_full_path))
                or (conditional_send == "always")
        ):
            return True
        else:
            return False
    if source_file_name_match_type == "regex_match":
        file_names = find_all_local_file_names(source_folder_name)
        matching_file_names = find_all_file_matches(
            file_names, re.compile(source_file_name)
        )
        if (
                (conditional_send == "file_exists" and len(matching_file_names) > 0)
                or (conditional_send == "file_dne" and len(matching_file_names) == 0)
                or (conditional_send == "always")
        ):
            return True
        else:
            return False


def main():
    args = get_args()
    destination_type = args.destination_type
    channel_name = args.channel_name
    message = args.message
    user_lookup_method = args.user_lookup_method
    users_to_notify = args.users_to_notify
    file_upload = args.file_upload
    source_file_name = args.source_file_name
    source_folder_name = clean_folder_name(args.source_folder_name)
    source_full_path = file_utils.combine_folder_and_file_name(source_folder_name, source_file_name)

    source_file_name_match_type = args.source_file_name_match_type

    conditional_send = args.conditional_send
    include_in_thread = args.include_file_in_thread == "yes"

    if should_message_be_sent(
            conditional_send,
            source_folder_name,
            source_file_name,
            source_file_name_match_type,
    ):
        shipyard_link = create_shipyard_link()
        slack_client = SlackClient(args.slack_token)
        if users_to_notify:
            user_id_list = create_user_id_list(
                slack_client, users_to_notify, user_lookup_method
            )
        else:
            user_id_list = []

        if destination_type == "dm":
            for user_id in user_id_list:
                if file_upload == "yes":
                    file_to_upload = determine_file_to_upload(
                        source_file_name_match_type,
                        source_folder_name,
                        source_file_name,
                    )
                    send_slack_message_with_file(
                        slack_client,
                        message,
                        user_id,
                        shipyard_link,
                        file_to_upload,
                        include_file_in_thread=include_in_thread,
                    )
                else:
                    send_slack_message(
                        slack_client,
                        message,
                        user_id,
                        create_blocks(message, shipyard_link),
                    )

        else:
            names_to_tag = create_name_tags(user_id_list)
            message = names_to_tag + message

            if file_upload == "yes":
                file_to_upload = file_utils.find_matching_files(source_file_name,
                                                                source_folder_name,
                                                                source_file_name_match_type)

                send_slack_message_with_file(
                    slack_client,
                    message,
                    channel_name,
                    shipyard_link,
                    file_to_upload,
                    include_file_in_thread=include_in_thread,
                )
            else:
                message_response = send_slack_message(
                    slack_client,
                    message,
                    channel_name,
                    create_blocks(message, shipyard_link),
                )
    else:
        if conditional_send == "file_exists":
            print("File(s) could not be found. Message not sent.")
        if conditional_send == "file_dne":
            print(
                "File(s) were found, but message was conditional based on file not existing. Message not sent."
            )


if __name__ == "__main__":
    main()
