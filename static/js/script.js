// script.js
$(document).ready(function () {
    function validateInputs() {
        let isValid = true;
        $(".error-message").remove();
        $(".is-invalid").removeClass("is-invalid");

        // Validate duration
        const duration = parseInt($("#predictionDuration").val());
        if (isNaN(duration) || duration <= 0) {
            showError($("#predictionDuration"), "Duration must be at least 1 day");
            isValid = false;
        }

        // Validate amount
        const amount = parseFloat($("#predictionAmount").val());
        if (isNaN(amount) || amount <= 0) {
            showError($("#predictionAmount"), "Investment must be greater than ₹0");
            isValid = false;
        }

        return isValid;
    }

    function showError(element, message) {
        element.addClass("is-invalid");
        element.after(`<div class="error-message text-danger small mt-1">${message}</div>`);
    }

    function fetchData(url, containerId, callback) {
        $.getJSON(url, function (data) {
            if (data.error) {
                $(containerId).html(`<p class="text-danger">${data.error}</p>`);
            } else {
                callback(data);
            }
        });
    }

    // Fetch Stock News
    $("#fetchNews").click(function () {
        let stock = $("#stockName").val().trim();
        if (stock === "") {
            alert("Please enter a stock name!");
            return;
        }

        fetchData(`/get_news?stock=${encodeURIComponent(stock)}`, "#newsContainer", function (data) {
            let newsHTML = data.map(article => `
                <div class="news-item">
                    <h5><a href="${article.link}" target="_blank">${article.title}</a></h5>
                    <p><strong>Sentiment:</strong> ${article.sentiment} (Score: ${article.score.toFixed(2)})</p>
                </div>
            `).join("");
            $("#newsContainer").html(newsHTML);
        });
    });

    // Fetch Technical Indicators (Price Chart, RSI Chart, MACD Chart & Volume Analysis)
    $("#fetchIndicators").click(function () {
        let stock = $("#techStock").val();
        $.getJSON(`/get_technical_indicators?stock=${stock}`, function (data) {
            if (data.error) {
                $("#priceChartContainer").html(`<p class="text-danger">${data.error}</p>`);
                $("#rsiChartContainer").html("");
                $("#macdChartContainer").html("");
                $("#volumeChartContainer").html("");
            } else {
                $("#priceChartContainer").html(data.price_chart);
                $("#rsiChartContainer").html(data.rsi_chart);
                $("#macdChartContainer").html(data.macd_chart);
                $("#volumeChartContainer").html(data.volume_chart);
            }
        });
    });

    // Fetch Candlestick Chart
    $("#fetchCandlestick").click(function () {
        let stock = $("#candlestickStock").val();
        fetchData(`/get_candlestick_chart?stock=${stock}`, "#candlestickContainer", function (data) {
            $("#candlestickContainer").html(data.image);
        });
    });
    
    //Stock Predictions
    $("#fetchPrediction").click(function () {
        let stock = $("#predictionStock").val();
        let duration = $("#predictionDuration").val() || 365;
        let amount = $("#predictionAmount").val() || 1000;
        
        $.getJSON(`/predict_stock?stock=${stock}&duration=${duration}&amount=${amount}`, function (data) {
            if (data.error) {
                $("#predictionChartContainer").html(`<p class="text-danger">${data.error}</p>`);
            } else {
                $("#predictionChartContainer").html(data.graph);
            }
        });
    });

    //chatbot
    $("#send-btn").click(function () {
        let userMessage = $("#chat-input").val();
        if (userMessage.trim() === "") return;

        $("#chat-box").append(`<div class="chat-message user-message">${userMessage}</div>`);
        $("#chat-input").val("");

        $.ajax({
            type: "POST",
            url: "/chatbot",
            data: { message: userMessage },
            success: function (response) {
                $("#chat-box").append(`<div class="chat-message bot-message">${response.response}</div>`);
                $("#chat-box").scrollTop($("#chat-box")[0].scrollHeight);
            }
        });
    });
});