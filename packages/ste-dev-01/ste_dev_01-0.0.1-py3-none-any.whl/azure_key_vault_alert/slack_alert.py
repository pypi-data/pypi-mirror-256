#!/usr/bin/env python

import logging


def split_msg(title, kv, max_chars, slack_app=False):
    results = []
    cb = ""
    if slack_app:
        cb = "```"

    # The summary payload is created first
    summary = kv.get_markdown_summary()
    if slack_app:
        payload = {"text": f"*{title} - summary*\n{cb}{summary}{cb}"}
        results.append(payload)
    else:
        results.append((f"{title} - summary", summary))

    # Then the report is split into chucks
    report = kv.get_markdown_report_only()
    report_lines = report.splitlines()

    # The two first line of the report is the header, which will now be used in every part
    header = f"{cb}{report_lines.pop(0)}\n{report_lines.pop(0)}\n"

    # Now the first part of the first report payload is initialized
    part = 1
    txt = ""
    payload = {"text": f"*{title} - Part {part}*\n{header}"}

    # Now we parse through every line of data in the report and add it to individual payloads
    # When a payload have reacted its max size, a new payload is initialized
    for line in report_lines:
        if len(txt) <= max_chars:
            txt += f"{line}\n"
            payload["text"] += f"{line}\n"
        else:
            if slack_app:
                payload["text"] += cb
                results.append(payload)
            else:
                results.append((f"{title} - Part {part}", f"{header}{txt}"))

            part += 1
            txt = f"{line}\n"
            payload = {"text": f"*{title} - Part {part}*\n{header}{txt}"}

    # If the remaining payload consists of more than the heading, it will also be added to the list of payloads
    if txt:
        if slack_app:
            payload["text"] += cb
            results.append(payload)
        else:
            results.append((f"{title} - Part {part}", f"{header}{txt}"))

    logging.info(f"Message was split into {len(results)} chunks.")

    return results


def slack_alert(title, kv, slack_app=False, stdout_only=False, msg_handler=None):
    """generates a json payload from 'title' and 'report' and then post the payload
     the url set in the WEBHOOK_REPORT variable

    Parameters
    ----------
    title : str
        The title of the message
    report : str
        The report part of the message
    slack_app : bool
        Create Slack app payload if set to True, else it will build a payload for Slack Webflow
    Returns
    -------
    True
        If response from the POST has return code 200
    """

    # Get full report, including the top summary
    report = kv.get_markdown_report()

    # Return if no report
    if not isinstance(report, str):
        logging.warning("No report")
        return

    # If stdout_only we print the report to standard output only and then return
    if stdout_only or not msg_handler:
        print(title)
        print(report)
        return

    # Set the max length of a Slack Workflow message and a Slack App message
    # If above these values the message will be split to multiple messages
    max_chars = 3500
    success_counter = 0

    # SLACK APP
    # If posting to a Slack app the payload is created accordingly
    if slack_app:
        logging.info("Building payload for Slack App..")
        payloads = [{"text": f"*{title}*\n```{report}```"}]

        # If the payload is too large for the Slack App it will be split into multiple posts
        if len(str(payloads)) > max_chars:
            logging.info("The message will be to large. Splitting up into chunks..")
            payloads = split_msg(title, kv, max_chars, slack_app=slack_app)

        logging.info(f"{len(payloads)} payloads will be posted..")
        for p in payloads:
            msg_handler.set_payload(p)
            msg_handler.post_payload()

            # If any of the payloads are sent it is considered a success
            response_code = msg_handler.get_response_code()
            if isinstance(response_code, int) and response_code == 200:
                success_counter += 1
            else:
                logging.error(f"Failed to send message to Slack App. Response code {str(response_code)}.")

        # Return True if success so that we know at least one message have been sent
        if success_counter:
            logging.info(f"{success_counter} messages posted to the Slack app.")
            return True

        return

    # SLACK WORKFLOW
    # If posting to a Slack Workflow the payload is build by the Message Handler
    logging.info("Building payload for Slack Workflow..")

    # If the payload is too large for the Slack App it will be split into multiple posts
    if len(report) > max_chars:
        logging.info("The message will be to large. Splitting up into chunks..")
        posts = split_msg(title, kv, max_chars, slack_app=slack_app)

        logging.info(f"{len(posts)} post will be posted..")
        for title_, text_ in posts:
            msg_handler.build_payload(Title=title_, Text=text_)
            msg_handler.post_payload()

            # If any of the payloads are sent it is considered a success
            response_code = msg_handler.get_response_code()
            if isinstance(response_code, int) and response_code == 200:
                success_counter += 1
            else:
                logging.error(f"Failed to send message to Slack Workflow. Response code {str(response_code)}.")

        # Return True if success so that we know at least one message have been sent
        if success_counter:
            logging.info(f"{success_counter} messages posted to the Slack Workflow.")
            return True

        return
