use dashmap::DashMap;
use log::error;
use mappings::MAPPINGS;
use ropey::Rope;
use tower_lsp::jsonrpc::{Error, Result};
use tower_lsp::lsp_types::notification::PublishDiagnostics;
use tower_lsp::lsp_types::{
    Diagnostic, DiagnosticSeverity, DidChangeTextDocumentParams,
    DidCloseTextDocumentParams, DidOpenTextDocumentParams,
    DidSaveTextDocumentParams, DocumentDiagnosticParams,
    DocumentDiagnosticReportResult, InitializeParams, InitializeResult,
    InitializedParams, MessageType, Position, PublishDiagnosticsParams, Range,
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

        let warnings = rope.lines().enumerate().flat_map(|(row, line)| {
            line.chars().enumerate().filter_map(move |(col, c)| {
                MAPPINGS.get(&c).map(|correct| {
                    Diagnostic::new(
                        Range::new(
                            Position::new(row as u32, col as u32),
                            Position::new(row as u32, col as u32 + 1),                        ),
                        Some(DiagnosticSeverity::WARNING),
                        None,
                        None,
                        format!("Character `{}` ({}) could be confused with the ASCII character `{}`({})", 
                        c, c.escape_unicode(), correct, correct.escape_unicode()),
                        None,
                        None,
                    )
                })
            })
        });

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
        documents: Default::default(),
    });
    Server::new(stdin, stdout, socket).serve(service).await;
}
