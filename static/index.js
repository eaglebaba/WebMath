document.addEventListener('DOMContentLoaded', init);

function init() {

    /*
     * Define variables for canvas element.
     * =====================================================================
     * getCanvas :->  returns all canvas objects
     * setCanvas :->  prepares the canvas for drawing
     * findxy    :->  returns the position of the mouse
     * draw      :->  does the actual drawing
     *
     */

    var canvas1, canvas2, canvas3, ctx1,
        ctx2, ctx3, w1, h1, w2, h2, w3, h3, x , y,
        prevX, currX, prevY, currY, dot_flag, flag;
        // x = line color (strokestyle), y = line width ( linewidth )
        prevX=0; currX=0; prevY=0; currY=0; dot_flag=false; x="white"; y=4;

    function getCanvas(id){
        var canvas = document.getElementById(id);
        var ctx = canvas.getContext("2d")
        ctx.fillStyle = "#000";
        w = canvas.width;
        h = canvas.height;
        ctx.fillRect(0, 0, w, h);
        return [canvas, ctx, w, h]
    }

    function draw(ctx) {
        ctx.beginPath();
        ctx.moveTo(prevX, prevY);
        ctx.lineTo(currX, currY);
        ctx.strokeStyle = x;
        ctx.lineWidth = y;
        ctx.stroke();
        ctx.closePath();
    }

    function setCanvas(canvas, ctx){
        canvas.addEventListener("mousemove", function (e) {
            findxy('move', e, canvas, ctx)
        }, false);
        canvas.addEventListener("mousedown", function (e) {
            findxy('down', e, canvas, ctx)
        }, false);
        canvas.addEventListener("mouseup", function (e) {
            findxy('up', e, canvas, ctx)
        }, false);
        canvas.addEventListener("mouseout", function (e) {
            findxy('out', e, canvas, ctx)
        }, false);
    }

    function findxy(res, e, canvas, ctx) {
        if (res == 'down') {
            prevX = currX;
            prevY = currY;
            currX = e.clientX - canvas.offsetLeft;
            currY = e.clientY - canvas.offsetTop;
    
            flag = true;
            dot_flag = true;
            if (dot_flag) {
                ctx.beginPath();
                ctx.fillStyle = x;
                ctx.fillRect(currX, currY, 2, 2);
                ctx.closePath();
                dot_flag = false;
            }
        }
        if (res == 'up' || res == "out") {
            flag = false;
        }
        if (res == 'move') {
            if (flag) {
                prevX = currX;
                prevY = currY;
                currX = e.clientX - canvas.offsetLeft;
                currY = e.clientY - canvas.offsetTop;
                draw(ctx);
            }
        }
    }

    function erase(ctx, w, h){
        ctx.fillStyle = "#000"
        ctx.fillRect(0, 0, w, h);
    }

    function saveCanvasToImg(canvas1, canvas2, canvas3){
        document.getElementById('working_loader').style.display = 'block';
        var img1 = canvas1.toDataURL("image/png");
        var math_symbol = canvas2.toDataURL("image/png");
        var img2 = canvas3.toDataURL("image/png");
        var img_data = {};
        img_data['img1'] = img1;
        img_data['math_symbol'] = math_symbol;
        img_data['img2'] = img2;
        img_data = JSON.stringify(img_data);

        var xhr = new XMLHttpRequest();
        var url = "http://127.0.0.1:5000/solve";
        xhr.open("POST", url, true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function(){
            if (xhr.readyState === 4 && xhr.status === 200) {
                response = JSON.parse(xhr.responseText);
                console.log(response)
                // hide the working loader after receiving the response
                document.getElementById('working_loader').style.display = 'none';

                document.getElementById('first_prediction').textContent = response['num_1'];
                document.getElementById('first_percentage').textContent = response['num_1_perc'];

                document.getElementById('operation_prediction').textContent = response['op'];
                document.getElementById('operation_percentage').textContent = response['op_perc'];

                document.getElementById('second_prediction').textContent = response['num_2'];
                document.getElementById('second_percentage').textContent = response['num_2_perc'];

                document.getElementById('ans').textContent = response['solution'];
            }
        }
        xhr.send(img_data);
    }

// =========================================================================== //
    [canvas1, ctx1, w1, h1] = getCanvas("canvas1");
    [canvas2, ctx2, w2, h2] = getCanvas("canvas2");
    [canvas3, ctx3, w3, h3] = getCanvas("canvas3");

    setCanvas(canvas1, ctx1);
    setCanvas(canvas2, ctx2);
    setCanvas(canvas3, ctx3);

    // prepare canvases for erasing
    document.getElementById("btn_clear").addEventListener("click", function(){
        erase(ctx1, w1, h1);
        erase(ctx2, w2, h2);
        erase(ctx3, w3, h3);
    });

    // prepare canvases for submission
    document.getElementById("btn_solve").addEventListener("click", function(){
        // grab all three images at the same time and send to server
        // i.e. saveCanvasToImg(canvas1, canvas2, canvas3);
        saveCanvasToImg(canvas1, canvas2, canvas3);
    });

}
