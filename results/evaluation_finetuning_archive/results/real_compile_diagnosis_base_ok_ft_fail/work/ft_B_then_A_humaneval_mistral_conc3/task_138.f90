program is_equal_to_sum_even
      implicit none
      integer :: n
      logical :: result
      n = 4
      result = is_equal_to_sum_even(n)
      print *, result
    contains
      logical function is_equal_to_sum_even(n)
        if (mod(n, 2) == 0 .and. n >= 8) then
           is_equal_to_sum_even = .true.
        else
           is_equal_to_sum_even = .false.
        end if
      end function is_equal_to_sum_even
    end program is_equal_to_sum_even