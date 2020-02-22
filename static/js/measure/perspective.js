// 各種DOMの取得
const utils = new Utils("errorMessage");
const imageUsed = document.getElementById("target").getAttribute("src");
const applyButton = document.getElementById("apply");
const submitButton = document.getElementById("fix");
let image_data = document.getElementById("id_image_data");

// 確定ボタンの設定
const setUpApplyButton = function() {
  let pointsArray = [];
  const children = document.querySelectorAll("#window_g .handle");

  // 各ハンドルから点の座標を取得し、配列に入れる
  children.forEach(e => {
    const pos = e.getAttribute("transform");
    const point = pos
      .replace("translate(", "")
      .replace(")", "")
      .split(",");
    pointsArray.push(point[0]);
    pointsArray.push(point[1]);
  });

  // 原本のイメージを一回表示する
  utils.loadImageToCanvas(imageUsed, "imageInit");

  setTimeout(() => {
    let src = cv.imread("imageInit");
    const imageHeight = document.getElementById("imageInit").height;
    const imageWidth = document.getElementById("imageInit").width;
    const svgCropHeight =
      document.querySelector("#background svg").getAttribute("height") - 80;
    const svgCropWidth =
      document.querySelector("#background svg").getAttribute("width") - 80;
    const scaleFactor = parseInt(imageWidth / svgCropWidth);
    pointsArray = pointsArray.map(e => {
      const num = parseInt((parseInt(e) + 40) / scaleFactor);
      return num;
    });

    //// 画像の幾何学変換を行うためのデータを取得し設定する
    let dst = new cv.Mat();
    let dsize = new cv.Size(500, 707);
    let srcTri = cv.matFromArray(4, 1, cv.CV_32FC2, pointsArray);
    let dstTri = cv.matFromArray(4, 1, cv.CV_32FC2, [
      0,
      0,
      500,
      0,
      500,
      707,
      0,
      707
    ]);

    //// イメージの幾何学変換を行う
    // 透視変換
    let M = cv.getPerspectiveTransform(srcTri, dstTri);
    cv.warpPerspective(
      src,
      dst,
      M,
      dsize,
      cv.INTER_LINEAR,
      cv.BORDER_CONSTANT,
      new cv.Scalar()
    );

    //　変換した結果をDOMに表示
    document.getElementById("imageInit").style.display = "none";
    cv.imshow("imageResult", dst);
    src.delete();
    dst.delete();
    M.delete();
    srcTri.delete();
    dstTri.delete();
    submitButton.classList.toggle("hidden");
  }, 500);
};

// 画像変換時に確定ボタンの操作を一時的に不可にする
applyButton.setAttribute("disabled", "true");
applyButton.onclick = setUpApplyButton;
utils.loadOpenCv(() => {
  setTimeout(function() {
    applyButton.removeAttribute("disabled");
  }, 500);
});

// フォームの処理
$("#main-form").submit(function(e) {
  var form = this;
  e.preventDefault();

  //// スクリーンショットを取る
  let canvas = document.getElementById("imageResult");

  document.getElementById("blur").style.display = "flex";
  setTimeout(function() {
    image_data_value = canvas.toDataURL("image/jpg");
    image_data.value = image_data_value;
    setTimeout(function() {
      form.submit();
    }, 1000);
  }, 500);
});
