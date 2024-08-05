const path = require('path')
const AdmZip = require('adm-zip')

exports.default = async function(context) {
  let targetPath
  if(context.packager.platform.nodeName === 'darwin') {
    targetPath = path.join(context.appOutDir, `${context.packager.appInfo.productName}.app/Contents/Resources`)
  } else {
    targetPath = path.join(context.appOutDir, './resources')
  }
  const unpacked = path.join(targetPath, './app.asar.unpacked')
  const zip = new AdmZip("", undefined);
  zip.addLocalFolder(unpacked)
  zip.writeZip(path.join(context.outDir, 'unpacked.zip'))
}
