var fs = require('fs');
var request = require('request');
var path = require('path');
var execSync = require('exec-sync');

var url = 'http://sunshine.cy.gov.tw/GipOpenWeb/wSite/sp?xdUrl=/wSite/SpecialPublication/baseList.jsp&ctNode=';
var pdfUrl = 'http://sunshine.cy.gov.tw/GipOpenWeb/wSite/SpecialPublication/fileDownload.jsp?id=';
var mly = JSON.parse(fs.readFileSync('mly-8.json', {encoding: 'utf8'}));
const RE_DOWNLOAD = /javascript:redirectFileDownload\((\d+)\)/gm;


mly.forEach(function(ly) {

  request.post(url, {
    form: {
      nowPage: '1',
      perPage: '300',
      queryStr: ly.name,
      queryCol: 'name'
    }
  }, function (error, response, body) {
    console.log(ly.name);
    if (!fs.existsSync('data')) {
      fs.mkdirSync('data');
    }
    var targetDir = path.join('data', ly.name);
    if (!fs.existsSync(targetDir)) {
      fs.mkdirSync(targetDir);
    }
    var matched;
    while((matched = RE_DOWNLOAD.exec(body)) !== null) {
      var cmd = 'wget -c -O ' + path.join(targetDir, matched[1] + '.pdf')+ ' ' + pdfUrl+matched[1];
      console.log("cmd: " + cmd);
      try {
        execSync(cmd) ;
      } catch (e) {}
    }
  });
})
