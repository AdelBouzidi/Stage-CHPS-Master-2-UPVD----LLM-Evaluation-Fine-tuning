program even_odd_count_demo
  implicit none
  integer :: num
  integer :: even_count, odd_count
  character(len=1) :: digit

  ! Read input number
  read(*,*) num

  ! Initialize counters
  even_count = 0
  odd_count = 0

  ! Convert number to string and count digits
  write(num, '(I0)') num
  read(num, '(A)') digit

  ! Count even and odd digits
  do while (num /= 0)
    digit = mod(num, 10)
    if (mod(digit, 2) == 0) then
      even_count = even_count + 1
    else
      odd_count = odd_count + 1
    end if
    num = num / 10
  end do

  ! Output results
  print *, even_count, odd_count

end program even_odd_count_demo