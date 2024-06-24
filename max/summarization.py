from utils.environment import get_env

key = get_env("LANGUAGE_KEY")
endpoint = get_env("LANGUAGE_ENDPOINT")

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import AbstractiveSummaryAction


# Example method for summarizing text
def summarize(docs: list, max_sentence_count: int = 5):
    # Auth
    client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    poller = client.begin_analyze_actions(
        docs,
        actions=[AbstractiveSummaryAction(max_sentence_count=max_sentence_count)],
        language="fr",
    )

    document_results = poller.result()
    res = []
    for result in document_results:
        extract_summary_result = result[0]  # first document, first result
        if extract_summary_result.is_error:
            print(
                "...Is an error with code '{}' and message '{}'".format(
                    extract_summary_result.code, extract_summary_result.message
                )
            )
        else:
            res.append(extract_summary_result.summaries[0].text)

    return res
