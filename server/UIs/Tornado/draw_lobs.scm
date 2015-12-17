(define (compute-point-array angle height width)
  ; TRIG SECTION
  (define pi 3.14159)
  ; Transform angle
  (set! angle (- angle 90))
  ; Convert angle from degrees to radians
  (define angle_rad (/ (* angle pi) 180))

  ; Calculate coordinates for LOB
  (define lob_len height)
  (define start_x (round (/ width 2)))
  (define start_y height)
  ; For angle between 0 and 180, draw from top of image
  ; (Remember I rotated the initial angle by -90 degrees)
  (if (> angle 0)
    (if (< angle 180)
      (define start_y 0)))
  (define end_x (+ (* (cos angle_rad) lob_len) start_x))
  (define end_y (+ (* (sin angle_rad) lob_len) start_y))

  ; Set up small array of 2 points
  (define method-pts (cons-array 4 'double))
  (aset method-pts 0 start_x)
  (aset method-pts 1 start_y)
  (aset method-pts 2 end_x)
  (aset method-pts 3 end_y)
)


(define (script-fu-draw-lineofbearing angle)
  ; CHANGE ME: LOB length
  (define lob_length 750)
  (define width (* 2 lob_length))
  (define height lob_length)
  ; Make angle an integer
  (set! angle (round angle))

  ;(gimp-image-undo-group-start image)
  ;(gimp-image-new width height RGB)
  (let* ((image (car(gimp-image-new width height RGB)))
         (layer (car(gimp-layer-new image width height RGBA-IMAGE "lob" 100 NORMAL-MODE)))
        )
    (gimp-layer-add-alpha layer)

    ; TODO: Use (gimp-version) to check version and use the appropriate function below
    ;(gimp-image-insert-layer image layer 0 0)   ; Works with Gimp 2.8
    (gimp-image-add-layer image layer 0)        ; Works with Gimp 2.6.9

    ; CHANGE ME: foreground = LOB color; brush (val) = LOB thickness
    (gimp-context-set-foreground '(0 200 0))
    ; CHANGE ME: LOB thickness - Circle (01)/(03)/(05)/(07)/(09)/(11)
    (gimp-context-set-brush "Circle (03)")
    (gimp-context-set-background '(0 0 0))
    (gimp-context-set-opacity 100)
    (gimp-display-new image)


    ; Let's draw some LOBs!!
    (define png-filename (string-append "lob_" (number->string angle) ".png"))
    (define pts (compute-point-array angle height width))
    (gimp-pencil layer 4 pts)
    (gimp-displays-flush)   ; Demo didn't have this here but I want it before save
    (file-png-save-defaults RUN-NONINTERACTIVE image layer png-filename "")

    ; ATTEMPT TO AUTOMATE
    ; Create list of angles to draw
    ;(define angle_array '(0 5 10 15 20 25 30 35 40 45 50 55 60 65 70 75 80 85 90 95
    ;  100 105 110 115 120 125 130 135 140 145 150 155 160 165 170 175 180 185 190 195
    ;  200 205 210 215 220 225 230 235 240 245 250 255 260 265 270 275 280 285 290 295
    ;  300 305 310 315 320 325 330 335 340 345 350 355))
    ;(while (<> (length angle_array) 0)
    ;(set! curr_angle (car angle_array))
    ;(pts (compute-points-array curr_angle height width))
    ;(define pts (compute-point-array curr_angle height width))
    ;(gimp-pencil layer 4 pts)
    ;(gimp-paintbrush-default layer 1 (cons-array ;TODO: NEED AN ARRAY HERE )) 
    ;(gimp-displays-flush)   ; Demo didn't have this here but I want it before save
    ;(png-filename (string-append "lob_" curr_angle ".png"))
    ;(file-png-save-defaults RUN-NONINTERACTIVE image layer png-filename "")
    ;(set! angle_array (cdr angle_array))
    ;)
    ;)
  )

  ;(gimp-image-undo-group-end image)
  ;(gimp-displays-flush)
)

(script-fu-register
  "script-fu-draw-lineofbearing"        ;   Name of the script
  "<Image>/Filters/Draw LOBs"           ;   "<Image>/Tools/Paint Tools/Draw LOBs" ;   Where to put our script in the menus
  "Draw multiple Lines of Bearing"      ;   Simple description of script
  "jayemar"                             ;   Author name   
  "jayemar"                             ;   Copyright info
  "Feb 2014"                            ;   Date written
  "RGB*, GRAY*"                         ;   Which image modes to apply to (RGB, GRAY, INDEX)
  ; CHANGE ME: Uncomment the line below (and do some other stuff) to select angle at runtime
  SF-ADJUSTMENT "Angle (degrees)" '(0 0 355 5 5 0 0)
)
