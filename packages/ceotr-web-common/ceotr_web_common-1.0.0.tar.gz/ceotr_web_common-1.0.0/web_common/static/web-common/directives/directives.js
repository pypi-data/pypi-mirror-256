// Will likely split this if it expands

function scrollMarkup($timeout) {
    //This function will fire an event when the container/document is scrolled to the bottom of the page
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {

            var propToWatch = attrs.scrollMarkup;
            var el = element[0];

            scope.$watch(propToWatch, updateScrollability);
            element.bind("scroll", updateScrollLocation);

            function updateScrollability() {
                $timeout(function() {
                    if(el.scrollHeight == el.offsetHeight) {
                        element.removeClass('has-scroll');
                        element.addClass('no-scroll');
                    } else {
                        element.removeClass('no-scroll');
                        element.addClass('has-scroll');
                    }
                }, 0);
            }

            function updateScrollLocation() {
                if(el.scrollTop + el.offsetHeight >= el.scrollHeight) {
                    element.addClass('scrolled-bottom');
                } else {
                    element.removeClass('scrolled-bottom');
                }

                if(el.scrollTop == 0) {
                    element.addClass('scrolled-top');
                } else {
                    element.removeClass('scrolled-top');
                }
            }
        }
    };
}

function enterPressed() {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {

            element.bind("keydown keypress", function (event) {
                var keyCode = event.which || event.keyCode;

                // If enter key is pressed
                if (keyCode === 13) {
                    scope.$apply(function () {
                        // Evaluate the expression
                        scope.$eval(attrs.enterPressed);
                    });

                    event.preventDefault();
                }
            });
        }
    };
}

function mobileMenu() {
    return {
        restrict: 'A',
        link: function (scope, element) {
            var clicked = false;

            $(element).prepend('<li class="mobile-menu"><a><i class="fas fa-bars"></i></a></li>');

            $(window).click(function() {
                if(clicked) {
                    element.addClass('active');
                    clicked = false
                } else {
                    element.removeClass('active');
                }
            });
            $(element).find('li.mobile-menu').click(function () {
                clicked = true;
            });
        }
    };
}

function clickActive() {
    return {
        restrict: 'A',
        link: function (scope, element) {
            var clicked = false;

            $(window).click(function() {
                if(clicked) {
                    element.addClass('active');
                    clicked = false
                } else {
                    element.removeClass('active');
                }
            });
            $(element).click(function () {
                clicked = true;
            });
        }
    };
}

function showMore($window, $timeout) {
    return {
        restrict: 'A',
        link: function (scope, element) {
            var $linkEl = $(`<a href>More</a>`);
            var $parentEl = $(element[0].parentNode);
            $parentEl.append($linkEl);

            var showMore = false;

            var adjustLinkVisibility = function() {
                if(isOverflown(element[0])) {
                    $linkEl.show();
                } else {
                    $linkEl.hide();
                }
            };

            angular.element($window).bind('resize', adjustLinkVisibility);
            $timeout(adjustLinkVisibility, 500);

            $linkEl.on('click', function(e) {
                showMore = !showMore;

                if(showMore){
                    element.addClass('show-more');
                    $linkEl.text('Less');
                } else {
                    element.removeClass('show-more');
                    $linkEl.text('More');
                }

                e.preventDefault();
            });
        }
    };
}

function versionSrc($compile) {
    return {
        restrict: 'A',
        link: function (scope, element, attr) {
            var fullUrl = attr.versionSrc + '?v=' + SiteReference.buildNumber;
            element.attr('ng-src', fullUrl);
            element.removeAttr('version-src');
            $compile(element)(scope);
        }
    };
}

function wagtailStream(staticUrl) {
    var templatePath = staticUrl + 'web-common/directives/wagtail-stream.html';
    return function () {
        return {
            restrict: 'E',
            scope: {
                blocks: '=',
            },
            templateUrl: templatePath,
        };
    };
}
