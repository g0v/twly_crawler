var fs = require('fs');
var async = require('async');
var lq = require('./lq');
var RE_NAME = /.{3}(.{3})(.+?)(\d{4})(\d{4})/

var properties = JSON.parse(fs.readFileSync('property.json', {encoding: 'utf8'}));

var tasks = properties.map(function(property, index) {
  var match;
  if (property.property_category === 'land' &&
    property.name.substr(0, 3) === '臺北市' &&
    property.name.slice(-2) === '地號' &&
    !property.present_value &&
    (matched = RE_NAME.exec(property.name))) {
    var admit = matched[1];
    var sec = matched[2];
    var lid = [matched[3], matched[4]];
    return function(callback) {
      console.log("legislator_name: " + property.legislator_name);
      console.log("name: " + property.name);
      try {
        lq.query(admit, sec, lid, function(presentValue) {
          if (!presentValue) {
            callback(null, null);
            return;
          }
          console.log("presentValue: " + presentValue);
          properties[index].present_value = presentValue;
          fs.writeFileSync('property.json', JSON.stringify(properties, null, 2));
          callback(null, null);
          return;
        });
      } catch (e) {
        callback(null, null);
      }

    }
  } else {
    return function(callback) {
      callback(null, null);
      return;
    };
  }
});

async.series(tasks);
