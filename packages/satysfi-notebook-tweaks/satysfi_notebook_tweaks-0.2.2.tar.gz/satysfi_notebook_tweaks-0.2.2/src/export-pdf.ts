import { JupyterFrontEnd } from '@jupyterlab/application';
import { MainAreaWidget } from '@jupyterlab/apputils';
import { NotebookPanel } from '@jupyterlab/notebook';
import { IRenderMimeRegistry, MimeModel } from '@jupyterlab/rendermime';
import { KernelMessage } from '@jupyterlab/services';

export const exportPDF = async (
  app: JupyterFrontEnd,
  rendermime: IRenderMimeRegistry
) => {
  const nb = app.shell.currentWidget;
  if (!(nb instanceof NotebookPanel) || !nb.model) {
    return;
  }
  const workingKernel = nb.sessionContext.session?.kernel;
  if (!workingKernel) {
    return;
  }

  const cells = nb.model.sharedModel.cells.filter(
    ({ cell_type }) => cell_type === 'code'
  );
  const mods = cells
    .map(({ source }) => source)
    .filter(source => source.startsWith('%!'));
  const document = cells
    .filter(
      ({ source }) =>
        !source.startsWith('%!') &&
        !source.startsWith('%?') &&
        !source.startsWith('%%')
    )
    .map(({ source }) => source)
    .join('\n');

  const startKernel = app.serviceManager.kernels.startNew(
    {
      name: workingKernel.name
    },
    {
      clientId: workingKernel.clientId,
      username: workingKernel.username,
      handleComms: workingKernel.handleComms
    }
  );
  const renderingKernel = await ['%% render-in-pdf', ...mods].reduce(
    async (acc, code) =>
      acc.then(
        renderingKernel =>
          new Promise((resolve, reject) => {
            const future = renderingKernel.requestExecute({ code });
            future.onIOPub = msg => {
              if (
                KernelMessage.isStatusMsg(msg) &&
                msg.content.execution_state === 'idle'
              ) {
                resolve(renderingKernel);
              }

              if (KernelMessage.isErrorMsg(msg)) {
                reject(new Error(msg.content.evalue));
              }
            };
          })
      ),
    startKernel
  );
  const future = renderingKernel.requestExecute({ code: document });
  future.onIOPub = msg => {
    if (!KernelMessage.isExecuteResultMsg(msg)) {
      return;
    }

    renderingKernel.shutdown();
    const pdf = rendermime.createRenderer('application/pdf');
    const tab = new MainAreaWidget({
      content: pdf
    });
    tab.title.label = `PDF Export: ${nb.title.label}`;
    tab.id = `${nb.id}-exported-pdf`;
    tab.revealed.then(() => {
      pdf.renderModel(new MimeModel(msg.content));
    });
    app.shell.add(tab, 'main', { mode: 'tab-after' });
  };
};
