/** @odoo-module **/

import { CalendarController } from "@web/views/calendar/calendar_controller";
import { patch } from "@web/core/utils/patch";

patch(CalendarController.prototype, "hospital_management.CalendarController", {
    setup() {
        this._super(...arguments);

        // Добавляем нашу кнопку в календарь
        const generateButton = {
            type: "button",
            className: "btn btn-primary",
            label: "Generate Schedule",
            icon: "fa-calendar",
            callback: () => this._onGenerateSchedule(),
        };

        // Добавляем кнопку в элементы экшенов
        this.actionButtons.push(generateButton);
    },

    // Метод для обработки нажатия на кнопку
    _onGenerateSchedule() {
        // Открываем ваш визард при нажатии на кнопку
        this.do_action({
            type: "ir.actions.act_window",
            name: "Generate Doctor Schedule",
            res_model: "hospital_management.doctor.schedule.wizard",
            views: [[false, "form"]],
            target: "new",
        });
    },
});