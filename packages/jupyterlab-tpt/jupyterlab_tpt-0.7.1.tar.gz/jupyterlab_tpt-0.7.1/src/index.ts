/*
 * for attaching keybindings later on, see
 * https://towardsdatascience.com/how-to-customize-jupyterlab-keyboard-shortcuts-72321f73753d
 */

/* eslint-disable prettier/prettier */

import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application'

import { ICommandPalette } from '@jupyterlab/apputils'

import {
  INotebookTracker,
  Notebook,
  NotebookActions
} from '@jupyterlab/notebook'

import { CodeCell, MarkdownCell, Cell } from '@jupyterlab/cells'

// md_clean may be broken
import {
  md_get,
  md_insert,
  md_remove
} from 'jupyterlab-celltagsclasses'
import { ISettingRegistry } from '@jupyterlab/settingregistry'

import { Scope, apply_on_cells } from 'jupyterlab-celltagsclasses'

import selectedCellsCss from '../style/selected_cells.raw.css'

const PLUGIN_ID = 'jupyterlab-tpt:plugin'

// regarding hide-input, forget about the nbclassic behaviour
// we will just run once hideinput-to-hidecell
// and be done with it

// cells that have this in their code
const NEEDLE = 'tools.sample_from'

const set_remove_input_needle = (cell: Cell, hidden: boolean) => {
  // ignore text cells
  if (cell instanceof CodeCell) {
    // need to access the cell model
    const model = cell.model
    if (model.sharedModel.getSource().toLowerCase().indexOf(NEEDLE) !== -1) {
      if (hidden) {
        md_remove(cell, 'tags', 'remove-input')
      } else {
        md_insert(cell, 'tags', 'remove-input')
      }
    }
  }
}

// use depth=0 to remove
const make_text_and_insert_section = (notebook: Notebook, depth: number) => {
  // console.log("make_text_and_insert_section", depth)
  NotebookActions.changeCellType(notebook, 'markdown')
  const activeCell = notebook?.activeCell
  if (activeCell === undefined) {
    return
  }
  const model = activeCell?.model
  if (model === undefined) {
    return
  }
  // remove starting #'s if any
  for (let i = 4; i > 0; i--) {
    model.sharedModel.setSource(
      model.sharedModel.getSource().replace('#'.repeat(i) + ' ', '')
    )
  }
  if (depth === 0) {
    return
  }
  model.sharedModel.setSource(
    `${'#'.repeat(depth)} ${model.sharedModel.getSource()}`
  )
}

const toggle_tag = (cell: Cell, tag: string) => {
  if (md_get(cell, 'tags', tag)) {
    md_remove(cell, 'tags', tag)
  } else {
    md_insert(cell, 'tags', tag)
  }
}
/**
 * Initialization data for the jupyterlab-tpt extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-tpt:plugin',
  autoStart: true,
  requires: [ICommandPalette, INotebookTracker, ISettingRegistry],
  activate: (
    app: JupyterFrontEnd,
    palette: ICommandPalette,
    notebookTracker: INotebookTracker,
    settingRegistry: ISettingRegistry
  ) => {
    console.log('JupyterLab extension jupyterlab-tpt is activating')
    // console.log('ICommandPalette', palette)
    // console.log('INotebookTracker', notebookTracker)

    // the addCommand would accept the following
    // isEnabled: () => true,
    // isVisible: () => true,
    // iconClass: 'some-css-icon-class',
    // also we could pass args to execute, but in the hide-input case
    // it does not work well as we need distinct labels depending on the args

    // https://lumino.readthedocs.io/en/1.x/api/commands/interfaces/commandregistry.ikeybindingoptions.html
    // The supported modifiers are: Accel, Alt, Cmd, Ctrl, and Shift. The Accel
    // modifier is translated to Cmd on Mac and Ctrl on all other platforms. The
    // Cmd modifier is ignored on non-Mac platforms.
    // Alt is option on mac

    let [outline_selected_cells] = [false]

    let command

    // Option-Command-9 = toggle (hide-input) on all selected cells
    // Ctrl-Alt-9 = show (wrt hide-input) on all selected cells
    command = 'convenience:show-settings'
    app.commands.addCommand(command, {
      label: 'show settings',
      execute: () =>
        console.log(
          `Current settings: outline_selected_cells = ${outline_selected_cells}`
        )
    })
    palette.addItem({ command, category: 'Convenience' })
    // app.commands.addKeyBinding({ command, keys: ['Alt Cmd 7'], selector: '.jp-Notebook' })

    command = 'convenience:hide-input-all-samples'
    app.commands.addCommand(command, {
      label: `remove input for all code cells that contain ${NEEDLE}`,
      execute: () =>
        apply_on_cells(notebookTracker, Scope.All, cell =>
          set_remove_input_needle(cell, true)
        )
    })
    palette.addItem({ command, category: 'convenience' })
    app.commands.addKeyBinding({
      command,
      keys: ['Alt Cmd 8'],
      selector: '.jp-Notebook'
    })

    command = 'convenience:show-input-all-samples'
    app.commands.addCommand(command, {
      label: `reinstate input for all code cells that contain ${NEEDLE}`,
      execute: () =>
        apply_on_cells(notebookTracker, Scope.All, cell =>
          set_remove_input_needle(cell, false)
        )
    })
    palette.addItem({ command, category: 'convenience' })
    app.commands.addKeyBinding({
      command,
      keys: ['Ctrl Alt 8'],
      selector: '.jp-Notebook'
    })

    // Ctrl-0 to Ctrl-4 to set markdown sections
    for (let depth = 0; depth < 5; depth++) {
      command = `convenience:section-level-${depth}`
      app.commands.addCommand(command, {
        label: `active cell becomes section level ${depth}`,
        execute: () => {
          const notebook = notebookTracker.currentWidget?.content
          if (notebook === undefined) {
            return
          }
          make_text_and_insert_section(notebook, depth)
        }
      })
      palette.addItem({ command, category: 'convenience' })
      app.commands.addKeyBinding({
        command,
        keys: [`Ctrl ${depth}`],
        selector: '.jp-Notebook'
      })
    }

    // render-all-cells - unrender-all-cells (markdown actually)

    const unrender_markdown = (cell: Cell) => {
      if (cell.model.type !== 'markdown') {
        return
      }
      ;(cell as MarkdownCell).rendered = false
    }
    command = 'notebook:unrender-all-markdown'
    app.commands.addCommand(command, {
      label: 'unrender all markdown cells',
      execute: () =>
        apply_on_cells(notebookTracker, Scope.All, unrender_markdown)
    })
    palette.addItem({ command, category: 'convenience' })
    // control-e means end of ine if in edit mode
    app.commands.addKeyBinding({
      command,
      keys: ['Ctrl E'],
      selector: '.jp-Notebook.jp-mod-commandMode'
    })

    app.commands.addKeyBinding({
      command: 'notebook:render-all-markdown',
      keys: ['Ctrl W'],
      selector: '.jp-Notebook'
    })

    // this is actually lowercase u and d, would need an explicit Shift otherwise
    app.commands.addKeyBinding({
      command: 'notebook:move-cell-up',
      keys: ['U'],
      selector: '.jp-Notebook.jp-mod-commandMode'
    })
    app.commands.addKeyBinding({
      command: 'notebook:move-cell-down',
      keys: ['D'],
      selector: '.jp-Notebook.jp-mod-commandMode'
    })

    command = 'convenience:toggle-raises-exception'
    app.commands.addCommand(command, {
      label: 'toggle raises-exception for all selected cells',
      execute: () =>
        apply_on_cells(notebookTracker, Scope.Multiple, cell =>
          toggle_tag(cell, 'raises-exception')
        )
    })
    palette.addItem({ command, category: 'convenience' })
    app.commands.addKeyBinding({
      command,
      keys: ['Alt Cmd 6'],
      selector: '.jp-Notebook'
    })

    command = 'convenience:set-raises-exception'
    app.commands.addCommand(command, {
      label: 'set raises-exception for all selected cells',
      execute: () =>
        apply_on_cells(notebookTracker, Scope.Multiple, cell =>
          md_insert(cell, 'tags', 'raises-exception')
        )
    })
    palette.addItem({ command, category: 'convenience' })
    app.commands.addKeyBinding({
      command,
      keys: ['Ctrl Alt 6'],
      selector: '.jp-Notebook'
    })

    const apply_outline_selected_cells = (outline_selected_cells: boolean) => {
      const id = 'outline-selected-cells-style'
      const present = document.getElementById(id)
      // already good
      if (
        (outline_selected_cells && present) ||
        (!outline_selected_cells && !present)
      ) {
        return
      }
      // need to inject
      if (outline_selected_cells) {
        console.log('injecting css for outlining selection')
        const inject_css = (css_text: string, id: string) => {
          const style = document.createElement('style')
          style.setAttribute('type', 'text/css')
          style.id = id
          style.appendChild(document.createTextNode(css_text))
          document.body.appendChild(style)
        }
        inject_css(selectedCellsCss, id)
      } else {
        console.log('removing css for outlining selection')
        present?.remove()
      }
    }
    function loadSetting(setting: ISettingRegistry.ISettings): void {
      // Read the settings and convert to the correct type
      outline_selected_cells = setting.get('outline_selected_cells')
        .composite as boolean

      console.log(
        `tpt extension, outline_selected is read as ${outline_selected_cells}`
      )
      apply_outline_selected_cells(outline_selected_cells)
    }

    Promise.all([app.restored, settingRegistry.load(PLUGIN_ID)]).then(
      ([_, setting]) => {
        loadSetting(setting)
        setting.changed.connect(loadSetting)
      }
    )
  }
}

export default plugin
