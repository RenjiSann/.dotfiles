import os
from os import path
import logging

import pytest_lsp
from lsprotocol.types import (
    InitializeParams,
    DidOpenTextDocumentParams,
    TextDocumentItem,
    TEXT_DOCUMENT_PUBLISH_DIAGNOSTICS,
)
from pytest_lsp import (
    ClientServerConfig,
    LanguageClient,
    client_capabilities,
)

LOGGER = logging.getLogger()

EXE_PATH = path.abspath(
    path.join(path.realpath(__file__), "../../target/debug/mischar")
)
FIXTURES_PATH = path.abspath(path.join(path.realpath(__file__), os.pardir, "fixtures"))


@pytest_lsp.fixture(
    config=ClientServerConfig(
        server_command=["/bin/bash", "-c", EXE_PATH],
    ),
)
async def client(lsp_client: LanguageClient):
    # Setup
    response = await lsp_client.initialize_session(
        InitializeParams(
            capabilities=client_capabilities("neovim"),
            root_uri=f"file://{FIXTURES_PATH}",
        )
    )

    yield

    # Teardown
    await lsp_client.shutdown_session()


async def test_diagnostics(client: LanguageClient):
    """Ensure that the server implements diagnostics correctly."""

    test_uri = f"file://{FIXTURES_PATH}/test1.txt"
    client.text_document_did_open(
        DidOpenTextDocumentParams(
            text_document=TextDocumentItem(
                uri=test_uri,
                language_id="plaintext",
                version=1,
                text="−The file's contents",
            )
        )
    )

    # Wait for the server to publish its diagnostics
    await client.wait_for_notification(TEXT_DOCUMENT_PUBLISH_DIAGNOSTICS)

    assert test_uri in client.diagnostics
    LOGGER.info(client.diagnostics)
