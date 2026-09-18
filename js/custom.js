jQuery(document).ready(function ($) {
  function toggleCompanyPullDown($li) {
    var $list = $li.closest(".wf-company-select");
    var opening = !$li.hasClass("is-open");
    $list.children("li.is-open").not($li).each(function () {
      $(this).removeClass("is-open")
        .find(".wf-co-toggle").attr("aria-expanded", "false")
        .end().find(".wf-co-profile").stop(true, true).slideUp(200);
    });
    if (opening) {
      $li.addClass("is-open");
      $li.find(".wf-co-toggle").attr("aria-expanded", "true");
      $li.find(".wf-co-profile").stop(true, true).slideDown(220);
    } else {
      $li.removeClass("is-open");
      $li.find(".wf-co-toggle").attr("aria-expanded", "false");
      $li.find(".wf-co-profile").stop(true, true).slideUp(200);
    }
  }

  $(".wf-company-select").on("click", ".wf-co-toggle", function (e) {
    if ($(e.target).closest("a").length) return;
    toggleCompanyPullDown($(this).closest("li"));
  });

  $(".wf-company-select").on("keydown", ".wf-co-toggle", function (e) {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      toggleCompanyPullDown($(this).closest("li"));
    }
  });

  $(".carousel").not("#article-photo-carousel").carousel({ interval: 5500 });

  var $gal = $("#article-photo-carousel");
  if ($gal.length) {
    $gal.carousel({ interval: false });
    loadProjectGallery($gal);
  }

  function photoExists(url) {
    return new Promise(function (resolve) {
      var img = new Image();
      img.onload = function () { resolve(true); };
      img.onerror = function () { resolve(false); };
      img.src = url;
    });
  }

  function rebuildProjectGallery($carousel, urls) {
    var inner = urls.map(function (url, i) {
      return '<div class="item' + (i === 0 ? ' active' : '') + '"><img alt="" src="' + url + '"></div>';
    }).join("");
    $carousel.find(".carousel-inner").html(inner);
    $carousel.find(".carousel-control, .carousel-indicators").remove();
    if (urls.length > 1) {
      $carousel.append(
        '<a class="left carousel-control" href="#article-photo-carousel" data-slide="prev"><i class="fa fa-angle-left"></i></a>' +
        '<a class="right carousel-control" href="#article-photo-carousel" data-slide="next"><i class="fa fa-angle-right"></i></a>'
      );
      var thumbs = urls.map(function (url, i) {
        return '<li class="' + (i === 0 ? "active" : "") + '" data-slide-to="' + i + '" data-target="#article-photo-carousel"><img alt="" src="' + url + '"></li>';
      }).join("");
      $carousel.append('<ol class="carousel-indicators wf-gallery-thumbs">' + thumbs + "</ol>");
    }
    $carousel.carousel({ interval: false });
  }

  function loadProjectGallery($carousel) {
    var src = $carousel.find(".carousel-inner img").first().attr("src") || "";
    var m = src.match(/^(.*\/)\d+\.(?:jpe?g|png|webp)(?:\?.*)?$/i);
    if (!m) return;
    var dir = m[1];
    var exts = [".jpg", ".jpeg", ".png", ".webp"];
    var urls = [];
    function existsAny(n) {
      return exts.reduce(function (p, ext) {
        return p.then(function (found) {
          if (found) return found;
          var url = dir + n + ext;
          return photoExists(url).then(function (ok) { return ok ? url : ""; });
        });
      }, Promise.resolve(""));
    }
    function next(n) {
      if (n > 40) {
        if (urls.length) rebuildProjectGallery($carousel, urls);
        return;
      }
      existsAny(n).then(function (url) {
        if (url) {
          urls.push(url);
          next(n + 1);
        } else if (urls.length) {
          rebuildProjectGallery($carousel, urls);
        }
      });
    }
    next(1);
  }
});
