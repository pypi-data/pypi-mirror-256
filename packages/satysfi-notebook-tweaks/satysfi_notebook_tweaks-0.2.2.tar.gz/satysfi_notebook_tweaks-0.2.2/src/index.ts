import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { ICommandPalette } from '@jupyterlab/apputils';
import { NotebookPanel } from '@jupyterlab/notebook';
import { IRenderMimeRegistry } from '@jupyterlab/rendermime';
import { CMD_EXPORT_PDF } from './consts';
import { exportPDF } from './export-pdf';

/**
 * Initialization data for the satysfi-notebook-tweaks extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'satysfi-notebook-tweaks:plugin',
  description: 'A small tweaks for SATySFi Notebook environment.',
  autoStart: true,
  requires: [ICommandPalette, IRenderMimeRegistry],
  activate: (
    app: JupyterFrontEnd,
    palette: ICommandPalette,
    rendermime: IRenderMimeRegistry
  ) => {
    app.commands.addCommand(CMD_EXPORT_PDF, {
      label: 'SATySFi Notebook: Export entire document as PDF',
      isVisible: () => {
        const widget = app.shell.currentWidget;
        return (
          widget instanceof NotebookPanel &&
          widget.sessionContext.kernelPreference.language?.toLowerCase() ===
            'satysfi'
        );
      },
      execute: () => exportPDF(app, rendermime)
    });

    palette.addItem({
      command: CMD_EXPORT_PDF,
      category: 'notebook'
    });
  }
};

export default plugin;
