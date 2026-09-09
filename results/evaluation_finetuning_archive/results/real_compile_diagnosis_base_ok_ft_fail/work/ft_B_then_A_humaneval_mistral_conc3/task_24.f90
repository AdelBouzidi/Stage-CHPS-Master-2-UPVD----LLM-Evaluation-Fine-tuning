program main
      implicit none
      integer :: n
      integer :: result
      n = 15
      result = largest_divisor(n)
      print *, result
    contains
      integer function largest_divisor(n)
        implicit none
        integer :: i
        result = n
        do i = 2, n/2
          if (mod(n, i) == 0) then
            result = i
          end if
        end do
      end function largest_divisor
    end program main