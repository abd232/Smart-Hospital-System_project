if (/Mobi/.test(navigator.userAgent)) {
  // if mobile device, use native pickers
  $(".date input").attr("type", "date");
} else {
  // if desktop device, use DateTimePicker
  $("#datepicker").datetimepicker({
    useCurrent: false,
    format: "DD-MMM-YYYY",
    showTodayButton: true,
    icons: {
      next: "fa fa-chevron-right",
      previous: "fa fa-chevron-left",
      today: 'todayText',
    }
  });
}