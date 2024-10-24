import pytest
from email.utils import parsedate_to_datetime
from google.cloud import bigquery as bq


@pytest.fixture()
def the_attachment_module(test_runner_service_account_credentials):
    # remember, first monkeypatch the credentials, then import the module,
    # and i'm not sure if type annotate the return defeat the purpose
    import attachment

    attachment.init()
    yield attachment
    del attachment


def test_table_creation(the_attachment_module):
    #
    client: bq.Client = the_attachment_module._client  # type: ignore
    project = the_attachment_module._project
    dataset = the_attachment_module._DATASET
    table_name = the_attachment_module._TABLE + "_test"
    the_attachment_module._TABLE = table_name

    client.delete_table(table=f"{project}.{dataset}.{table_name}", not_found_ok=True)

    the_attachment_module.create_table()

    client.delete_table(table=f"{project}.{dataset}.{table_name}", not_found_ok=False)


def test_insert(the_attachment_module):

    # row = history_id=0,
    #    project_id=project_id,
    #    message_id="19233f063eec1719",
    #    message_from="a@b.c",
    #    message_date=parsedate_to_datetime("27 Sep 2024 11:43:58 -0300"),
    #    message_subject="the subject",
    #    attachment_id="ANGjdJ_deHe7fENfIhMS1GHfH2zZ_Lw66velytd13TEvoFpbUVsT_xdujKFOKcL0l3O0gwmW3ihl3zTn1n1gUcLmzV_UV6Y7JlWNKr42RYCEaH0W60gCj9Ml7h5SWnpjHpjOZCDGEsA4yAc3-RnyUP7YmVzPWvzttqghoFcSa2JIj04lJlu-HJnmYlP1HX-qN014vYR3UiwT7U5Y-su8pDpzRYAibzOyyzzvBD6I0BLJ3opG5Q0O6CCz7wa8gEpSDAzWDfppa_gh8s2Oo0LMkq67wmDNnV-IrSnMCI7HecChpFYvDVTBz_CiJSKQzvPP48QZKoNmUAAv6TTCeCOlcwCViIM7F3QfW7X87s-0xw7mj0i-puswnpj5cRCJH-MQdP_yKPe0_YgJwUY_brww",
    #    filename="TUTEUR2309240817.TXT"

    client: bq.Client = the_attachment_module._client  # type: ignore
    project = the_attachment_module._project
    dataset = the_attachment_module._DATASET
    table_name = the_attachment_module._TABLE

    the_attachment_module.create_table()

    row = (
        0,
        "19233f063eec1719",
        "a@b.c",
        parsedate_to_datetime("27 Sep 2024 11:43:58 -0300"),
        "the subject",
        "ANGjdJ_deHe7fENfIhMS1GHfH2zZ_Lw66velytd13TEvoFpbUVsT_xdujKFOKcL0l3O0gwmW3ihl3zTn1n1gUcLmzV_UV6Y7JlWNKr42RYCEaH0W60gCj9Ml7h5SWnpjHpjOZCDGEsA4yAc3-RnyUP7YmVzPWvzttqghoFcSa2JIj04lJlu-HJnmYlP1HX-qN014vYR3UiwT7U5Y-su8pDpzRYAibzOyyzzvBD6I0BLJ3opG5Q0O6CCz7wa8gEpSDAzWDfppa_gh8s2Oo0LMkq67wmDNnV-IrSnMCI7HecChpFYvDVTBz_CiJSKQzvPP48QZKoNmUAAv6TTCeCOlcwCViIM7F3QfW7X87s-0xw7mj0i-puswnpj5cRCJH-MQdP_yKPe0_YgJwUY_brww",
        "TUTEUR2309240817.TXT",
    )

    the_attachment_module.insert(row)

    client.delete_table(table=f"{project}.{dataset}.{table_name}", not_found_ok=False)
