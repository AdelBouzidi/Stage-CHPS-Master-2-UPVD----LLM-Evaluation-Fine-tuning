program even_odd_palindrome_demo
  implicit none
  integer, parameter :: i4b = selected_int_kind(9)
  integer(i4b) :: n
  integer(i4b) :: even_count, odd_count
  
  ! Read input
  read(*,*) n
  
  ! Call the function
  call even_odd_palindrome(n, even_count, odd_count)
  
  ! Print output
  print *, even_count, odd_count
  
contains

  subroutine even_odd_palindrome(n, even_count, odd_count)
    implicit none
    integer(i4b), intent(in) :: n
    integer(i4b), intent(out) :: even_count, odd_count
    integer(i4b) :: i
    integer(i4b) :: is_palindrome
    
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
  end subroutine even_odd_palindrome

  function is_palindrome(num) result(is_palindrome)
    implicit none
    integer(i4b), intent(in) :: num
    integer(i4b) :: is_palindrome
    integer(i4b) :: temp, reversed
    integer(i4b) :: digit
    
    temp = num
    reversed = 0
    do
      digit = mod(temp, 10)
      reversed = reversed * 10 + digit
      temp = temp / 10
      if (temp == 0) exit
    end do
    is_palindrome = (num == reversed)
  end function is_palindrome

end program even_odd_palindrome_demo