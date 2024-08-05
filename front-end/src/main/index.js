import { app, shell, BrowserWindow, ipcMain } from 'electron'
import { join } from 'path'
import { electronApp, optimizer, is } from '@electron-toolkit/utils'
import icon from '../../resources/icon.png?asset'
import {checkForUpdates, hotUpdateApp} from "./HotUpdate";
import axios from "axios";
import * as path from "node:path";
import * as fs from "node:fs";

function createWindow() {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 900,
    height: 670,
    show: false,
    autoHideMenuBar: true,
    icon: join(__dirname,'../../resources/icon.png'),
    ...(process.platform === 'linux' ? { icon } : {}),
    webPreferences: {
      preload: join(__dirname, '../preload/index.js'),
      sandbox: false
    }
  })

  mainWindow.on('ready-to-show', () => {
    mainWindow.show()
  })

  mainWindow.webContents.setWindowOpenHandler((details) => {
    shell.openExternal(details.url)
    return { action: 'deny' }
  })

  // HMR for renderer base on electron-vite cli.
  // Load the remote URL for development or the local html file for production.
  if (is.dev && process.env['ELECTRON_RENDERER_URL']) {
    mainWindow.loadURL(process.env['ELECTRON_RENDERER_URL'])
  } else {
    mainWindow.loadFile(join(__dirname, '../renderer/index.html'))
  }
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  // Set app user model id for windows
  electronApp.setAppUserModelId('com.imusic')

  // Default open or close DevTools by F12 in development
  // and ignore CommandOrControl + R in production.
  // see https://github.com/alex8088/electron-toolkit/tree/master/packages/utils
  app.on('browser-window-created', (_, window) => {
    optimizer.watchWindowShortcuts(window)
  })

  // IPC
  ipcMain.handle('check-update', (event, args) => {
    return checkForUpdates(args)
  })
  ipcMain.handle('hot-update', async () => {
    await hotUpdateApp()
    const win = BrowserWindow.getFocusedWindow();
    await win.loadFile(join(__dirname, '../renderer/index.html'))
  })

  // 注册主进程的下载事件
  ipcMain.handle('downloadZip', async (event, args) => {
    const { DOWNLOAD_URL } = args; // 获取下载地址等参数
    const win = BrowserWindow.getFocusedWindow(); // 获取当前焦点的窗口

    try {
      // 发起请求下载压缩文件
      const response = await axios.get(DOWNLOAD_URL, {
        responseType: 'arraybuffer',  // 设置响应类型为二进制数据流
        onDownloadProgress: (progressEvent) => {
          // 发送下载进度给渲染进程
          win.webContents.send('downloadProgress', {
            loaded: progressEvent.loaded,
            total: progressEvent.total
          });
        }
      });

      // 将二进制数据保存为临时文件
      let tempZipFilePath = path.join(__dirname, 'temp.zip');
      if (!is.dev){
        tempZipFilePath = path.join(__dirname, '../../../temp.zip');
      }
      fs.writeFileSync(tempZipFilePath, response.data);

      console.log('Downloaded successfully.');
    } catch (error) {
      console.error('Error downloading files:', error);
    }
  });

  createWindow()

  app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

// In this file you can include the rest of your app"s specific main process
// code. You can also put them in separate files and require them here.
