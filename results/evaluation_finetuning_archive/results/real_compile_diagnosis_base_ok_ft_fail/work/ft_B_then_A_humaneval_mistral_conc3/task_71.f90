program triangle_area_main
      implicit none
      real :: a, b, c, area

      read(*,*) a
      read(*,*) b
      read(*,*) c

      if (a > 0.0 .and. b > 0.0 .and. c > 0.0 .and. &
          a + b > c .and. a + c > b .and. b + c > a) then
         area = sqrt( (a + b + c) / 2.0 * &
                      (a + b + c) / 2.0 - a * &
                      (a + b + c) / 2.0 - b * &
                      (a + b + c) / 2.0 - c )
      else
         area = -1.0
      end if

      print '(F6.2)', area

    end program triangle_area_main