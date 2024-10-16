odoo.define('your_module_name.date_picker', function (require) {
    'use strict';

    var FormView = require('web.FormView');
    var core = require('web.core');
    var QWeb = core.qweb;
    var _t = core._t;

    FormView.include({
        render_buttons: function ($node) {
            this._super($node);
            this.$('.o_field_widget[name="start_week"]').on('change', function () {
                var selectedDate = new Date($(this).val());
                // Проверка, является ли дата понедельником
                if (selectedDate.getDay() !== 1) {  // 1 соответствует понедельнику
                    alert(_t('Please select a Monday.'));
                    $(this).val('');  // Сброс выбора
                }
            });
        },
    });
});