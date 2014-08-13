function createquarter(myDocObj) {
    myDocObj = app.activeDocs[0];
    var pt2inch = 72;
    app.beginPriv();
    var ready = app.alert({
        cMsg: "Press Ok to select the west quarter section.  Press Cancel to quit.",
        cTitle: "Select a Quarter",
        nIcon: 3,
        nType: 1
    });
   if (ready == 2) {
	      var close = app.alert({
            cMsg: "Press Yes to cancel this operation.",
            cTitle: "Canceling...",
            nIcon: 1,
            nType: 2
        });
	      if(close == 3){
            this.closeDoc();
		  }
        } 
	else {
        var prompt = app.browseForDoc();
        this.addWatermarkFromFile({
            cDIPath: prompt.cPath, //west pdf
            nHorizAlign: 1, //left align
            nVertAlign: 4, //top align
            nHorizValue: pt2inch * -8, //72 per inch
            nVertValue: pt2inch * 3,
			bOnTop: false
        });
        ready = app.alert({
            cMsg: "Press Ok to select the east quarter section.  Press Cancel to quit.",
            cTitle: "Select a Quarter",
            nIcon: 3,
            nType: 1
        });
        if (ready == 2) {
	      close2 = app.alert({
            cMsg: "Press Yes to cancel this operation.",
            cTitle: "Canceling...",
            nIcon: 1,
            nType: 2
        });
	      if(close2 == 3){
            this.closeDoc();
		  }
        } else {
            var prompt2 = app.browseForDoc();
            this.addWatermarkFromFile({
                cDIPath: prompt2.cPath, //east pdf
                nHorizAlign: 3, //right align
                nVertAlign: 4,
                nHorizValue: pt2inch * 8,
                nVertValue: pt2inch * 3,
			    bOnTop: false
            });
            app.endPriv();
        }
    }
}
app.trustedFunction(createquarter);

function createhalf(myDocObj) {
    myDocObj = app.activeDocs[0];
    var pt2inch = 72;
    app.beginPriv();
    var ready = app.alert({
        cMsg: "Press Ok to select the half section.  Press Cancel to quit.",
        cTitle: "Select a Half",
        nIcon: 3,
        nType: 1
    });
    if (ready == 2) {
	  var close = app.alert({
          cMsg: "Press Yes to cancel this operation.",
          cTitle: "Canceling...",
          nIcon: 1,
          nType: 2
    });
	  if(close == 3){
        this.closeDoc();
		}
    } else {
        var prompt = app.browseForDoc();
        this.addWatermarkFromFile({
            cDIPath: prompt.cPath, //half pdf
            nHorizAlign: 1, //left align
            nVertAlign: 4, //top align
            nHorizValue: pt2inch * -0.5, //72 per inch
            nVertValue: pt2inch * 0,
			bOnTop: false
        });
        app.endPriv();
        }
    }

app.trustedFunction(createhalf);
