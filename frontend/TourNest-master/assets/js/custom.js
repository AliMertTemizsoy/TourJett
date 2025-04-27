$(document).ready(function(){

	"use strict";

    

        /*==================================

* Author        : "ThemeSine"

* Template Name : Travel HTML Template

* Version       : 1.0

==================================== */


        /*=========== TABLE OF CONTENTS ===========

1. Scroll To Top
2. Range js
3. Countdown timer
4. owl carousel
5. datepicker
6. Smooth Scroll spy
7. Animation support
======================================*/
    

    // 1. Scroll To Top 

		$(window).on('scroll',function () {

			if ($(this).scrollTop() > 600) {

				$('.return-to-top').fadeIn();

			} else {

				$('.return-to-top').fadeOut();

			}

		});

		$('.return-to-top').on('click',function(){

				$('html, body').animate({

				scrollTop: 0

			}, 1500);

			return false;

		});

    // 2. range js
        
        $( "#slider-range" ).slider({
            range: true,
            min: 0,
            max: 12000,
            values: [ 2677, 9241 ],
            slide: function( event, ui ) {
            $( "#amount" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
            }
        });
        $( "#amount" ).val( "$" + $( "#slider-range" ).slider( "values", 0 ) +
        " - $" + $( "#slider-range" ).slider( "values", 1 ) );
        
        
        // Quantity Buttons Shop
    
        $(".qtyplus").on("click", function(){
        var b = $(this).parents(".quantity-form").find("input.qty"),
                c = parseInt(b.val(), 10) + 1,
                d = parseInt(b.attr("max"), 10);
            d || (d = 9999999999), c <= d && (b.val(c), b.change())
        });
        $(".qtyminus").on("click", function(){
            var b = $(this).parents(".quantity-form").find("input.qty"),
                c = parseInt(b.val(), 10) - 1,
                d = parseInt(b.attr("min"), 10);
            d || (d = 1), c >= d && (b.val(c), b.change())
        });


    // 3.Countdown timer 
        
        function makeTimer() {

                var endTime = new Date("March 7, 2018 12:00:00 PDT");            
                var endTime = (Date.parse(endTime)) / 1000;

                var now = new Date();
                var now = (Date.parse(now) / 1000);

                var timeLeft = endTime - now;

                var days = Math.floor(timeLeft / 86400); 
                var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
                var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600 )) / 60);
                var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));

                if (hours < "10") { hours = "0" + hours; }
                if (minutes < "10") { minutes = "0" + minutes; }
                if (seconds < "10") { seconds = "0" + seconds; }

                $("#days").html(days + '<span class="camp">Days</span>');
                $("#hours").html(hours + '<span class="camp">Hour</span>');
                $("#minutes").html(minutes + '<span class="camp">Minute</span>');
                $("#seconds").html(seconds + '<span class="camp">Second</span>');       

        }
        
        setInterval(function() { makeTimer(); }, 1000);

    // 4. owl carousel
    
        // i. #testimonial-carousel
    
        
        var owl=$('#testemonial-carousel');
        owl.owlCarousel({
            items:3,
            margin:0,
            
            loop:true,
            autoplay:true,
            smartSpeed:1000,
            
            //nav:false,
            //navText:["<i class='fa fa-angle-left'></i>","<i class='fa fa-angle-right'></i>"],
            
            dots:true,
            autoplayHoverPause:true,
        
            responsiveClass:true,
                responsive:{
                    0:{
                        items:1
                    },
                    640:{
                        items:1
                    },
                    767:{
                        items:2
                    },
                    992:{
                        items:3
                    }
                }
            
            
        });

    // 5. datepicker
            $('[data-toggle="datepicker"]').datepicker();

    // 6. Smooth Scroll spy
        
        $('.header-area').sticky({
           topSpacing:0
        });
        
        //=============

        $('li.smooth-menu a').bind("click", function(event) {
            event.preventDefault();
            var anchor = $(this);
            $('html, body').stop().animate({
                scrollTop: $(anchor.attr('href')).offset().top - -1
            }, 1200,'easeInOutExpo');
        });
        
        $('body').scrollspy({
            target:'.navbar-collapse',
            offset:0
        });

    // 7.animation support

        $(window).load(function(){

            $(".about-us-txt h2").removeClass("animated fadeInUp").css({'opacity':'0'});
            $(".about-us-txt button").removeClass("animated fadeInDown").css({'opacity':'0'});
        });

        $(window).load(function(){

            $(".about-us-txt h2").addClass("animated fadeInUp").css({'opacity':'0'});
            $(".about-us-txt button").addClass("animated fadeInDown").css({'opacity':'0'});

        });

        async function loadTours() {
            try {
                const turlar = await getTurlar(); // api.js'den turları çek
                const container = $('#tour-container'); // HTML'de bu ID'li div olmalı
                turlar.forEach(tour => {
                    container.append(`
                        <div class="col-md-4 mb-4">
                            <div class="card">
                                <img src="${tour.resim}" class="card-img-top">
                                <div class="card-body">
                                    <h5 class="card-title">${tour.adi}</h5>
                                    <p class="card-text">${tour.aciklama}</p>
                                    <p class="text-success">${tour.fiyat} TL</p>
                                </div>
                            </div>
                        </div>
                    `);
                });
            } catch (error) {
                console.error('Tur verileri yüklenemedi:', error);
            }
        }
        loadTours(); // Sayfa açıldığında turları yükle
});	

// Tur paketlerini API'den çekmek için fonksiyon
function getTurlar() {
    console.log("Fetching tours from API...");
    return window.ApiService.tours.getAll()
        .then(response => {
            console.log("API Response:", response);
            return response;
        })
        .catch(error => {
            console.error("Error fetching tours:", error);
            throw error;
        });
}

// Tur paketlerini yükle
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM loaded, checking for packages container");
    // Tur paketlerini yükle
    const packagesContainer = document.querySelector('.packages-content');
    if (packagesContainer) {
        console.log("Packages container found, loading tour packages");
        // Yükleniyor mesajını göster
        packagesContainer.innerHTML = '<div class="text-center"><p>Turlar yükleniyor...</p></div>';
        
        // API'den tur paketlerini çek
        getTurlar()
            .then(data => {
                console.log('Tur verileri:', data);
                
                // HTML içeriği oluştur
                if (data && data.length > 0) {
                    let packagesHTML = '';
                    data.forEach(tur => {
                        packagesHTML += `
                            <div class="col-md-4 col-sm-6">
                                <div class="single-package-item">
                                    <img src="${tur.resim_url || 'assets/images/packages/default.jpg'}" alt="${tur.ad}">
                                    <div class="single-package-item-txt">
                                        <h3>${tur.ad} <span class="pull-right">${tur.fiyat}₺</span></h3>
                                        <div class="packages-para">
                                            <p>${tur.aciklama}</p>
                                            <p><span><i class="fa fa-clock-o"></i> ${tur.sure}</span></p>
                                        </div>
                                        <div class="packages-review">
                                            <p><i class="fa fa-map-marker"></i> ${tur.konum}</p>
                                        </div>
                                        <div class="about-btn">
                                            <a href="package-details.html?id=${tur.id}" class="about-view packages-btn">
                                                Şimdi Rezervasyon Yap
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        `;
                    });
                    
                    packagesContainer.innerHTML = packagesHTML;
                } else {
                    packagesContainer.innerHTML = '<div class="text-center"><p>Henüz tur paketi bulunmamaktadır.</p></div>';
                }
            })
            .catch(error => {
                console.error('Tur yükleme hatası:', error);
                packagesContainer.innerHTML = `<div class="text-center"><p>Turlar yüklenirken bir hata oluştu: ${error.message}</p></div>`;
            });
    } else {
        console.log("Packages container not found");
    }
});

