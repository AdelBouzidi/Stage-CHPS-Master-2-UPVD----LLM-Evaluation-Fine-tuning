program main
  implicit none
  integer :: num
  integer :: even_count, odd_count
  integer :: digit
  integer :: temp

  read(*,*) num

  if (num < 0) then
    temp = -num
  else
    temp = num
  end if

  even_count = 0
  odd_count = 0

  if (temp == 0) then
    even_count = 1
  else
    do while (temp > 0)
      digit = mod(temp, 10)
      if (mod(digit, 2) == 0) then
        even_count = even_count + 1
      else
        odd_count = odd_count + 1
      end if
      temp = temp / 10
    end do
  end if

  print *, even_count, odd_count

end program main