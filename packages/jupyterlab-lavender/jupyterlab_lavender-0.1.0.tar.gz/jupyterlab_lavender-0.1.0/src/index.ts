import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

/**
 * Initialization data for the jupyterlab_lavender extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab_lavender:plugin',
  description: 'JupyterLab theme extension with dark background and low saturation',
  autoStart: true,
  requires: [IThemeManager],
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    console.log('JupyterLab extension jupyterlab_lavender is activated!');
    const style = 'jupyterlab_lavender/index.css';

    manager.register({
      name: 'jupyterlab_lavender',
      isLight: false,
      load: () => manager.loadCSS(style),
      unload: () => Promise.resolve(undefined)
    });
  }
};

export default plugin;
