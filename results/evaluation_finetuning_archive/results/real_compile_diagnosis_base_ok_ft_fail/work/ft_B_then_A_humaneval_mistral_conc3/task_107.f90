program palindrome_count
      implicit none
      integer :: n
      integer :: even_count, odd_count
      integer :: i

      ! Read input
      read(*, *) n

      even_count = 0
      odd_count = 0

      do i = 1, n
         if (is_palindrome(i)) then
            if (mod(i, 2) == 0) then
               even_count = even_count + 1
            else
               odd_count = odd_count + 1
            end if
         end if
      end do

      print *, even_count, odd_count

    contains

      logical function is_palindrome(num)
        integer, intent(in) :: num
        character(len=12) :: str
        character(len=12) :: rev_str
        integer :: i, len_str

        write(str, '(I0)') num
        len_str = len_trim(str)
        do i = 1, len_str
           rev_str(i) = str(len_str - i + 1)
        end do
        is_palindrome = (str == rev_str)
      end function is_palindrome

    end program palindrome_count