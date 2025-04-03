from src.utils.slack import remove_slack_user_mentions  # Fix import for Slack utilities
from src.services.domo import domo_auth

import domolibrary.routes.workflows as workflow_routes
from slack_bolt.async_app import AsyncAck, AsyncSay
import os
from logging import Logger


async def trigger_domo_llms_workflow(question, channel_id, message_id, user_id):
    domo_starting_block = "Start HelpDeskMafia"
    domo_model_id = "48707704-213c-4c82-8a7d-69505b50a8de"
    domo_model_version_id = "1.0.9"

    execution_params = {
        "question": question,
        "channel_id": channel_id,
        "message_id": message_id,
        "user_id": user_id,
        "slack_token": os.environ["SLACK_BOT_TOKEN"],
    }

    return await workflow_routes.trigger_workflow(
        auth=domo_auth,
        starting_tile=domo_starting_block,
        model_id=domo_model_id,
        version_id=domo_model_version_id,
        execution_parameters=execution_params,
        debug_api=False,
    )


async def question_command_callback(
    command,
    ack: AsyncAck,
    say: AsyncSay,
    logger: Logger,
):
    await ack()
    logger.info(command)
    print("question_command_callback", command)

    user_id = command["user_id"]
    channel_id = command["channel_id"]
    clean_question = remove_slack_user_mentions(command["text"])
    # response_url = body["response_url"]

    said = await say(
        f'<@{user_id}> asked "{clean_question}"\nGive me a sec to think about it.  🌈',
        # channel=channel_id
    )

    await trigger_domo_llms_workflow(question=clean_question, channel_id=channel_id, message_id=said["ts"], user_id=user_id)
