program even_odd_palindrome
  implicit none
  integer :: n
  integer :: even_count, odd_count
  character(len=10) :: num_str
  integer :: i, len, j

  ! Read input
  read(*,*) n

  even_count = 0
  odd_count = 0

  do i = 1, n
    write(num_str, '(I0)') i
    len = len_trim(num_str)
    if (is_palindrome(num_str)) then
      if (mod(i, 2) == 0) then
        even_count = even_count + 1
      else
        odd_count = odd_count + 1
      end if
    end if
  end do

  print *, even_count, odd_count

contains

  logical function is_palindrome(str)
    character(len=*), intent(in) :: str
    integer :: len, i, j
    len = len_trim(str)
    do i = 1, len/2
      if (str(i:i) /= str(len-i+1:len-i+1)) then
        is_palindrome = .false.
        return
      end if
    end do
    is_palindrome = .true.
  end function is_palindrome

end program even_odd_palindrome