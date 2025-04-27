/*
* Monaco editor JS
* Monaco has a lot of configurations and logic related to the editor so it goes in it's own file
*/

// TODO: Add logic for either switching the basic template code comment or make it a DB field (IF SO THEN THAT GOES IN SERVICE LAYER)
let editor;
let saveTimeout;
let selected_language = document.getElementById('language-select').value;
let code_content = document.getElementById('monaco-editor').getAttribute('code-content');
let AUTOSAVE_DELAY = 1000;
require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs' }});
require(['vs/editor/editor.main'], function() {
    // Create and store the editor instance
    editor = monaco.editor.create(document.getElementById('monaco-editor'), {
    value: code_content,
    language: selected_language.toLowerCase(),
    theme: 'vs-light',
    minimap: { enabled: false },
    wordWrap: 'on',            
    wordWrapColumn: 0,
    wrappingIndent: 'same',
    automaticLayout: true,
    fontSize: 14,
    lineNumbers: 'on',
    glyphMargin: false,
    lineDecorationsWidth: 0,
    scrollBeyondLastLine: false,
    suggestOnTriggerCharacters: false,
    quickSuggestions: false,
    renderLineHighlight: 'none',
    hideCursorInOverviewRuler: true,
    overviewRulerLanes: 0,
    overviewRulerBorder: false,
    scrollbar: {
        vertical: 'visible',
        horizontal: 'visible',
        useShadows: false,
        verticalHasArrows: false,
        horizontalHasArrows: false,
        verticalScrollbarSize: 10,
        horizontalScrollbarSize: 10
        }
    });

    editor.onDidChangeModelContent(() => {
        // Clear previous timeout if it exists
        if (saveTimeout) {
          clearTimeout(saveTimeout);
        }
        
        // Set a new timeout to trigger save after user stops typing
        saveTimeout = setTimeout(() => {
          triggerAutosave();
        }, AUTOSAVE_DELAY);
      });

      document.getElementById('autosave-trigger').addEventListener('htmx:configRequest', function(event) {
        const content = editor.getValue();
        console.log(content);
        event.detail.parameters.content = content;
      });
    });

    function triggerAutosave() {
        // Dispatch a custom event that HTMX is listening for
        document.body.dispatchEvent(new CustomEvent('autosave-event'));
      }

// TODO: Add autosaving and update language switched without refreshing


  