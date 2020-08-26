$("#image-selector").change(function (){
    let reader = new FileReader();
    reader.onload = function(){
        let dataURL = reader.result;
        $('#selected-image').attr("src", dataURL);
        $('#selected-image').attr("style", "visibility:visible");
        $('#prediction-list').empty();
        $('#PredictionList').attr("style", "visibility:visible");
        $('#predict-button').attr("style", "visibility:visible");
    }
    let file = $("#image-selector").prop('files')[0];
    reader.readAsDataURL(file);
})


let model;
(async function loadModel(){
    model = await tf.loadLayersModel('http://localhost:3000/model/model.json');
    console.log("Model loaded!");
})()

$("#predict-button").click(async function(){
    console.log("Predict button clicked!");
    let image = $('#selected-image').get(0);
    const b = tf.scalar(255);

    let tensor = tf.browser.fromPixels(image).resizeNearestNeighbor([224, 224]).cast('float32').div(b).expandDims(0);

    let predictions = await model.predict(tensor).data();

    let top5 = Array.from(predictions).map(function(p, i){
        return {
            probability: p,
            className: CLASSES[i]
        };
    }).sort(function(a,b){
        return b.probability - a.probability;
    }).slice(0, 5);

    $("#prediction-list").empty();
    top5.forEach(function (p){
        $("#prediction-list").append(`<li>${p.className.charAt(0).toUpperCase()+p.className.slice(1).replace(/_/g, ' ')}: ${(p.probability*100).toFixed(2)} %</li>`);
    });
});
