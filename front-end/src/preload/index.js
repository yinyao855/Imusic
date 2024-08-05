import { contextBridge, ipcRenderer } from 'electron'
import { electronAPI } from '@electron-toolkit/preload'
import {join} from "path";

// Custom APIs for renderer
const api = {
  checkUpdateInfo (url) {
    return ipcRenderer.invoke('check-update', url)
  },
  hotUpdateApp () {
    return ipcRenderer.invoke('hot-update')
  }
}

// Use `contextBridge` APIs to expose Electron APIs to
// renderer only if context isolation is enabled, otherwise
// just add to the DOM global.
if (process.contextIsolated) {
  try {
    contextBridge.exposeInMainWorld('electron', electronAPI)
    contextBridge.exposeInMainWorld('api', api)

    // console.log('dirname:', __dirname)
    // console.log('renderer url:', join(__dirname, '../renderer/index.html'))
  } catch (error) {
    console.error(error)
  }
} else {
  window.electron = electronAPI
  window.api = api
}
