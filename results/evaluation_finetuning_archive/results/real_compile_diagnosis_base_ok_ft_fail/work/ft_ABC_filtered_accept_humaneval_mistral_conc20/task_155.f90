program even_odd_count_demo
  implicit none
  integer :: num
  integer :: even_count, odd_count
  integer :: digit
  integer :: abs_num

  ! Read input number
  read(*,*) num

  ! Get absolute value for digit counting
  abs_num = abs(num)

  ! Count even and odd digits
  even_count = 0
  odd_count = 0
  do while (abs_num > 0)
    digit = mod(abs_num, 10)
    if (mod(digit, 2) == 0) then
      even_count = even_count + 1
    else
      odd_count = odd_count + 1
    end if
    abs_num = abs_num / 10
  end do

  ! Output result
  print *, even_count, odd_count

end program even_odd_count_demo