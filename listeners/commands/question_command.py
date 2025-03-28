import os
from slack_bolt.async_app import AsyncAck, AsyncRespond, AsyncSay
import domolibrary.client.DomoAuth as dmda
import domolibrary.routes.filesets as fileset_routes
import utils

domo_auth = dmda.DomoTokenAuth(
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    domo_instance=os.environ["DOMO_INSTANCE"],
)


async def trigger_domo_llms_workflow(
    question,
    channel_id,
    message_id,
    user_id,
    debug_api: bool = False,
    slack_bot_token: str = None,
):
    domo_starting_block = "Start HelpDeskMafia"
    domo_model_id = "48707704-213c-4c82-8a7d-69505b50a8de"
    domo_model_version_id = "1.0.9"

    execution_params = {
        "question": question,
        "channel_id": channel_id,
        "message_id": message_id,
        "user_id": user_id,
        "slack_token": slack_bot_token or os.environ['SLACK_BOT_TOKEN'],
    }

    await fileset_routes.trigger_workflow(
        auth=domo_auth,
        starting_tile=domo_starting_block,
        model_id=domo_model_id,
        version_id=domo_model_version_id,
        execution_parameters=execution_params,
        debug_api=debug_api,
    )


async def question_command_callback(ack: AsyncAck, body, logger,
                                    say: AsyncSay):
    await ack()
    logger.info(body)
    # print("question_command_callback", body)

    user_id = body["user_id"]
    channel_id = body["channel_id"]
    question = utils.remove_slack_user_mentions(body["text"])
    # response_url = body["response_url"]

    print(channel_id)

    await say(
        f'<@{user_id}> asked: "{question}"\nGive me a sec to think about it.  🌈',
        # channel=channel_id
    )
