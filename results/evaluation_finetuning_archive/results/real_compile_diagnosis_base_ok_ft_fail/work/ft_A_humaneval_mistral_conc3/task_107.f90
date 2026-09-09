program even_odd_palindrome
  implicit none
  integer :: n
  integer :: even_count, odd_count
  integer :: i
  integer :: temp
  integer :: reversed
  integer :: digits(10)
  integer :: num_digits
  logical :: is_palindrome

  ! Read input
  read(*,*) n

  even_count = 0
  odd_count = 0

  do i = 1, n
    temp = i
    num_digits = 0
    digits(1) = 0
    do while (temp > 0)
      num_digits = num_digits + 1
      digits(num_digits) = mod(temp, 10)
      temp = temp / 10
    end do
    reversed = 0
    do num_digits, 1, 1
      reversed = reversed * 10 + digits(num_digits)
    end do
    if (i == reversed) then
      if (mod(i, 2) == 0) then
        even_count = even_count + 1
      else
        odd_count = odd_count + 1
      end if
    end if
  end do

  print *, even_count, odd_count

end program even_odd_palindrome