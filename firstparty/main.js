(function () {

    function getBasicInfo() {
        return {

                timeOpened:new Date(),
                timezone:(new Date()).getTimezoneOffset()/60,
                pageon: window.location.pathname,
                referrer: document.referrer,
                previousSites: history.length,
                browserName: navigator.appName,
                browserEngine: navigator.product,
                browserVersion1a: navigator.appVersion,
                browserVersion1b: navigator.userAgent,
                browserLanguage: navigator.language,
                browserOnline: navigator.onLine,
                browserPlatform: navigator.platform,
                javaEnabled: navigator.javaEnabled(),
                dataCookiesEnabled: navigator.cookieEnabled,
                dataCookies1: document.cookie,
                dataCookies2: decodeURIComponent(document.cookie.split(";")),
                dataStorage: localStorage,
            
                sizeScreenW: screen.width,
                sizeScreenH: screen.height,
                sizeDocW: document.body.clientWidth,
                sizeDocH: document.body.clientHeight,
                sizeInW: window.innerWidth,
                sizeInH: window.innerHeight,
                sizeAvailW: screen.availWidth,
                sizeAvailH: screen.availHeight,
                scrColorDepth: screen.colorDepth,
                scrPixelDepth: screen.pixelDepth
    
            };
    }

    function getMoreInfo() {
        return {

            timeOpened:new Date(),
            timezone:(new Date()).getTimezoneOffset()/60,
            
            referrer: document.referrer,
            previousSites: history.length,
            browserName: navigator.appName,
            browserEngine: navigator.product,
            browserVersion1a: navigator.appVersion,
            browserVersion1b: navigator.userAgent,
            browserLanguage: navigator.language,
            browserOnline: navigator.onLine,
            browserPlatform: navigator.platform,
            javaEnabled: navigator.javaEnabled(),
            dataCookiesEnabled: navigator.cookieEnabled,
            dataCookies1: document.cookie,
            dataCookies2: decodeURIComponent(document.cookie.split(";")),
            dataStorage: localStorage,
        
            sizeScreenW: screen.width,
            sizeScreenH: screen.height,
            sizeDocW: document.body.clientWidth,
            sizeDocH: document.body.clientHeight,
            
            sizeAvailW: screen.availWidth,
            sizeAvailH: screen.availHeight,
            scrColorDepth: screen.colorDepth,
            scrPixelDepth: screen.pixelDepth,
            pageon: window.location.pathname,
            sizeInW: window.innerWidth,
            sizeInH: window.innerHeight,

        };
    }

    function nonDefaultWindowVariable() {
        var results, currentWindow,
        // create an iframe and append to body to load a clean window object
        iframe = document.createElement('iframe');
        iframe.style.display = 'none';
        document.body.appendChild(iframe);
        // get the current list of properties on window
        currentWindow = Object.getOwnPropertyNames(window);
        // filter the list against the properties that exist in the clean window
        results = currentWindow.filter(function(prop) {
            return !iframe.contentWindow.hasOwnProperty(prop);
        });
        // log an array of properties that are different
        console.log(results);
        document.body.removeChild(iframe);
    }

    function getNavigatorInfo() {
        return {
            browserName: navigator.appName,
            browserEngine: navigator.product,
            browserVersion1a: navigator.appVersion,
            browserVersion1b: navigator.userAgent,
            browserLanguage: navigator.language,
            browserOnline: navigator.onLine,
            browserPlatform: navigator.platform,
            javaEnabled: navigator.javaEnabled(),
            dataCookiesEnabled: navigator.cookieEnabled,
            doNotTrack: navigator.doNotTrack,
            languages: navigator.languages,
            language: navigator.language,
            maxtouchpoints: navigator.maxTouchPoints,
            oscpu: navigator.oscpu,
            storage: navigator.storage,

        }
    }

    console.log(getBasicInfo());
    console.log(getMoreInfo());

    console.log(window);
    nonDefaultWindowVariable();

    console.log(document);

    console.log(navigator);
    console.log(getNavigatorInfo());

    console.log(screen);
})();