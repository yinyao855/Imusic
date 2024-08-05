import {is} from "@electron-toolkit/utils";

const axios = require('axios');
const AdmZip = require('adm-zip');
const fs = require('fs');
const path = require('path');

// 检查是否需要更新
export async function checkForUpdates(url) {
  try {
    // 发起请求检查是否有新版本
    const response = await axios.get(url, {
      timeout: 5000, // 设置超时时间为5秒
    });
    const {hasNewVersion} = response.data;
    if (hasNewVersion) {
      console.log('New version available.')
      return '有新版本可用'
    } else {
      console.log('Already up to date.')
      return '当前已是最新版本'
    }
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.code === 'ECONNABORTED') {
        console.error('Request timed out:', error);
        return '请求超时，请重试';
      } else {
        console.error('Axios error:', error.message);
      }
    } else {
      console.error('Error checking for updates:', error);
    }
    return '检查更新时出错，请重试';
  }
}

export async function hotUpdateApp() {
  try {
    let tempZipFilePath = path.join(__dirname, 'temp.zip');
    if (!is.dev){
      tempZipFilePath = path.resolve(__dirname, '../../../temp.zip');
    }

    // 先删除目标目录下的旧文件
    let targetDir = path.join(__dirname, '../renderer/');
    if (!is.dev){
      targetDir = path.join(__dirname, '../../../app.asar.unpacked/out/renderer/');
    }
    fs.rmSync(targetDir, {recursive: true});

    // 解压缩文件到目标目录
    const zip = new AdmZip(tempZipFilePath);
    let extractPath = path.join(__dirname, '../renderer/');
    if (!is.dev){
      extractPath = path.join(__dirname, '../../../app.asar.unpacked/out/renderer/');
    }
    zip.extractAllTo(extractPath, true);

    // 删除临时文件
    fs.unlinkSync(tempZipFilePath);

    console.log('Files extracted successfully.');
  } catch (error) {
    console.error('Error extracting files:', error);
  }
}
