program even_odd_palindrome
  implicit none
  integer :: n
  integer :: even_count, odd_count
  integer :: i
  integer :: temp, reversed

  ! Read input n
  read(*, *) n

  even_count = 0
  odd_count = 0

  do i = 1, n
    temp = i
    reversed = 0
    do while (temp > 0)
      reversed = reversed * 10 + mod(temp, 10)
      temp = temp / 10
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