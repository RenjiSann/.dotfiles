use dashmap::DashMap;
use log::error;
use ropey::Rope;
use tower_lsp::jsonrpc::{Error, Result};
use tower_lsp::lsp_types::notification::PublishDiagnostics;
use tower_lsp::lsp_types::{
    Diagnostic, DidChangeTextDocumentParams, DidCloseTextDocumentParams,
    DidOpenTextDocumentParams, DidSaveTextDocumentParams,
    DocumentDiagnosticParams, DocumentDiagnosticReport,
    DocumentDiagnosticReportResult, FullDocumentDiagnosticReport,
    InitializeParams, InitializeResult, InitializedParams, MessageType,
    PublishDiagnosticsParams, RelatedFullDocumentDiagnosticReport,
    TextDocumentItem,
};
use tower_lsp::{Client, LanguageServer, LspService, Server};

mod mappings;
mod scan;
mod utils;

#[derive(Debug)]
struct Backend {
    client: Client,
    diagnostics: DashMap<String, Vec<Diagnostic>>,
    documents: DashMap<String, Rope>,
}

impl Backend {
    async fn on_change(&self, params: TextDocumentItem) {

        let rope = Rope::from_str(&params.text);
        self.documents.insert(params.uri.to_string(), rope.clone());

        rope.lines().flat_map(|line| line);

        self.client
            .send_notification::<PublishDiagnostics>(
                PublishDiagnosticsParams::new(
                    params.uri.clone(),
                    self.diagnostics
                        .get(params.uri.as_str())
                        .as_deref()
                        .cloned()
                        .unwrap_or(vec![]),
                    params.version.into(),
                ),
            )
            .await
    }
}

#[tower_lsp::async_trait]
impl LanguageServer for Backend {
    async fn initialize(
        &self,
        _: InitializeParams,
    ) -> Result<InitializeResult> {
        Ok(InitializeResult::default())
    }

    async fn initialized(&self, _: InitializedParams) {
        self.client
            .log_message(MessageType::INFO, "server initialized!")
            .await;
    }

    async fn shutdown(&self) -> Result<()> {
        Ok(())
    }

    async fn did_open(&self, params: DidOpenTextDocumentParams) {
        self.on_change(TextDocumentItem {
            uri: params.text_document.uri,
            text: params.text_document.text,
            version: params.text_document.version,
            language_id: "plaintext".to_string(),
        })
        .await
    }

    async fn did_change(&self, mut params: DidChangeTextDocumentParams) {
        self.on_change(TextDocumentItem {
            uri: params.text_document.uri,
            text: std::mem::take(&mut params.content_changes[0].text),
            version: params.text_document.version,
            language_id: "plaintext".to_string(),
        })
        .await
    }

    async fn did_save(&self, _: DidSaveTextDocumentParams) {
        self.client
            .log_message(MessageType::INFO, "file saved!")
            .await;
    }
    async fn did_close(&self, _: DidCloseTextDocumentParams) {
        self.client
            .log_message(MessageType::INFO, "file closed!")
            .await;
    }

    async fn diagnostic(
        &self,
        params: DocumentDiagnosticParams,
    ) -> Result<DocumentDiagnosticReportResult> {
        panic!()
    }
}

#[tokio::main]
async fn main() {
    let stdin = tokio::io::stdin();
    let stdout = tokio::io::stdout();

    let (service, socket) = LspService::new(|client| Backend {
        client,
        diagnostics: Default::default(),
    });
    Server::new(stdin, stdout, socket).serve(service).await;
}