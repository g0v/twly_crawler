var fs = require('fs');
var request = require('request');
var Iconv  = require('iconv').Iconv;
var jsdom = require('jsdom');

var converter = new Iconv('Big5', 'UTF-8');
var arg, admit, sec, lid;

if (process.argv.length > 1) {
  var arg = process.argv[2].split(',');
  admit = arg[0];
  sec = arg[1];
  lid = arg[2].split('-');
}

var data = JSON.parse(fs.readFileSync('admit.json', {encoding: 'utf8'}));

var options = {
  url: 'http://tredb.taipei.gov.tw/TP95/newweb/sys/CASE/query_landno_show.cfm?typ=1',
  method: 'POST',
  encoding: null,
  form: {
    Admit_sel: data[admit].id,
    H_LSec: data[admit].sec[sec].id,
    LSec: data[admit].sec[sec].id,
    Lid_M: lid[0],
    Lid_S: lid[1],
    gaia: '1',
    query_from: 'landno',
    Table_Type: 'AREA',
    Table_Name: 'G67_A_LNPAR_P',
    FieldList: ' min(sdo_geom.sdo_min_mbr_ordinate(ORA_GEOMETRY,1)) X1,min(sdo_geom.sdo_min_mbr_ordinate(ORA_GEOMETRY,2)) Y1,max(sdo_geom.sdo_max_mbr_ordinate(ORA_GEOMETRY,1)) X2,max(sdo_geom.sdo_max_mbr_ordinate(ORA_GEOMETRY,2)) Y2 ',
    Where_Clause: '',
    NewWhereClause: '',
    NTable_Name: 'G67_A_LNPAR_P',
    ODBC_SRC: 'tp94-3'
  },
  headers: {
    'Referer': 'http://tredb.taipei.gov.tw'
  }
}

request(options, function(error, response, body) {
  var html = converter.convert(body);

  jsdom.env({
    html: html,
    scripts: ["http://code.jquery.com/jquery.js"],
    done: function (errors, window) {
      var $ = window.$;
      $('nobr').each(function() {
        if ($(this).text().trim() === '土地增值稅試算') {
          var parent = $(this).parent().parent();
          console.log("公告現值 (元/平方公尺): " + parent.children('nobr').text().split('[')[0]);
        }
      });
    }
  });
});
