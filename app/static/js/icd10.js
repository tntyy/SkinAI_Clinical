document.addEventListener('DOMContentLoaded', function () {

    var btn = document.getElementById('icdAnalyzeBtn');
    var panel = document.getElementById('icdAnalysisPanel');

    if (!btn || !panel) {
        return;
    }

    var loaded = false;

    btn.addEventListener('click', function () {

        // Nếu đã mở -> bấm lại để đóng
        if (panel.classList.contains('open')) {
            panel.classList.remove('open');
            return;
        }

        panel.classList.add('open');

        if (loaded) {
            return;
        }

        loadAnalysis();
    });

    function loadAnalysis() {

        panel.innerHTML =
            '<div class="icd-analysis-loading">' +
            '<div class="spinner-border spinner-border-sm text-primary" role="status"></div>' +
            '<span>Đang phân tích bằng AI...</span>' +
            '</div>';

        var code = btn.getAttribute('data-code');
        var nameVi = btn.getAttribute('data-name-vi');

        fetch('/doctor/icd10/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                code: code,
                name_vi: nameVi
            })
        })
            .then(function (res) {
                return res.json();
            })
            .then(function (data) {

                if (!data.success) {
                    renderError(data.message || 'Không thể phân tích bệnh này.');
                    return;
                }

                loaded = true;
                renderAnalysis(data);
            })
            .catch(function () {
                renderError('Không thể kết nối tới máy chủ phân tích AI.');
            });
    }

    function renderError(message) {

        panel.innerHTML =
            '<div class="icd-analysis-card warning full">' +
            '<div class="icd-analysis-card-title">' +
            '<i class="bi bi-exclamation-triangle"></i> Lỗi' +
            '</div>' +
            '<p>' + escapeHtml(message) + '</p>' +
            '</div>';
    }

    function renderList(items) {

        if (!items || !items.length) {
            return '<p>Chưa có dữ liệu.</p>';
        }

        var html = '<ul>';

        items.forEach(function (item) {
            html += '<li>' + escapeHtml(item) + '</li>';
        });

        html += '</ul>';

        return html;
    }

    function renderAnalysis(data) {

        var a = data.analysis || {};
        var treatment = a.treatment || {};

        var html = '';

        html += '<div class="icd-analysis-header">';
        html += '<i class="bi bi-robot"></i>';
        html += '<div>';
        html += '<h4>Phân tích: ' + escapeHtml(data.name_vi || '') + '</h4>';
        html += '<small>Phân tích bởi AI &middot; ' + escapeHtml(data.code || '') + '</small>';
        html += '</div>';
        html += '</div>';

        html += '<div class="icd-analysis-grid">';

        html += '<div class="icd-analysis-card">' +
            '<div class="icd-analysis-card-title"><i class="bi bi-question-circle"></i> Nguyên nhân</div>' +
            renderList(a.causes) +
            '</div>';

        html += '<div class="icd-analysis-card">' +
            '<div class="icd-analysis-card-title"><i class="bi bi-exclamation-diamond"></i> Yếu tố nguy cơ</div>' +
            renderList(a.risk_factors) +
            '</div>';

        html += '<div class="icd-analysis-card">' +
            '<div class="icd-analysis-card-title"><i class="bi bi-thermometer-half"></i> Triệu chứng lâm sàng</div>' +
            renderList(a.symptoms) +
            '</div>';

        html += '<div class="icd-analysis-card">' +
            '<div class="icd-analysis-card-title"><i class="bi bi-shield-exclamation"></i> Biến chứng</div>' +
            renderList(a.complications) +
            '</div>';

        html += '<div class="icd-analysis-card full">' +
            '<div class="icd-analysis-card-title"><i class="bi bi-capsule"></i> Hướng điều trị</div>' +
            '<div class="icd-treatment-tabs">' +
            '<span class="icd-treatment-tab">Thuốc</span>' +
            '<span class="icd-treatment-tab">Thủ thuật / can thiệp</span>' +
            '<span class="icd-treatment-tab">Lối sống</span>' +
            '</div>' +
            renderList(
                (treatment.medication || [])
                    .concat(treatment.procedure || [])
                    .concat(treatment.lifestyle || [])
            ) +
            '</div>';

        html += '<div class="icd-analysis-card full">' +
            '<div class="icd-analysis-card-title"><i class="bi bi-graph-up-arrow"></i> Tiên lượng</div>' +
            '<p>' + escapeHtml(a.prognosis || 'Chưa có dữ liệu.') + '</p>' +
            '</div>';

        html += '<div class="icd-analysis-card">' +
            '<div class="icd-analysis-card-title"><i class="bi bi-calendar2-check"></i> Cần theo dõi</div>' +
            renderList(a.follow_up) +
            '</div>';

        html += '<div class="icd-analysis-card warning">' +
            '<div class="icd-analysis-card-title"><i class="bi bi-exclamation-octagon"></i> Cảnh báo cấp cứu</div>' +
            renderList(a.emergency_warning) +
            '</div>';

        html += '</div>';

        panel.innerHTML = html;
    }

    function escapeHtml(text) {

        var div = document.createElement('div');
        div.textContent = text == null ? '' : text;
        return div.innerHTML;
    }

});