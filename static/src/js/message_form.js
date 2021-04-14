odoo.define('zalo_message.FormMessage', function (require) {
    'use strict';

    var test = require('mail/static/src/components/chatter_topbar/chatter_topbar.js');
    var fieldRegistry = require('web.field_registry');

    console.log(test)

    var FieldPad = test.extend({
        _onClickSendZaloMessage: function(){
            console.log('abc')
        }
    })

    fieldRegistry.add('pad', FieldPad);

    return FieldPad;

});
//
