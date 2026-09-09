program even_odd_count
  implicit none
  integer :: num
  integer :: even_count, odd_count
  integer :: temp

  ! Read input number
  read(*,*) num

  ! Initialize counters
  even_count = 0
  odd_count = 0

  ! Convert to absolute value for digit processing
  num = abs(num)

  ! Count even and odd digits
  do while (num > 0)
    temp = mod(num, 10)
    if (temp == 0 .or. temp == 2 .or. temp == 4 .or. temp == 6 .or. temp == 8) then
      even_count = even_count + 1
    else
      odd_count = odd_count + 1
    end if
    num = num / 10
  end do

  ! Output results
  print *, even_count, odd_count

end program even_odd_count