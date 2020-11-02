(function () {
    // The minimum prediction confidence.
    const threshold = 0.9;

    // Load the model. Users optionally pass in a threshold and an array of
    // labels to include.
    result = [0, 0, 0, 0, 0, 0, 0];
    toxicity.load(threshold).then(model => {
        const sentences = [];
        var start = 0;
        var end = sentences.length;

        function dodo () {
            if (start >= end) {
                console.log(result);
                return;
            }
            if (start == 2040) {
                console.log(result);
                return;
            }
            let i = start;
            let j = start + 1;

            start += 1;

            model.classify(sentences.slice(i, j)).then(predictions => {
                console.log(`${i}`);
                for (let p = 0; p < 7; p++) {
                    if (predictions[p]["results"][0]["match"]) {
                        result[p] += 1;
                    }
                }
                dodo();
            });
        };

        dodo();


    });
})();