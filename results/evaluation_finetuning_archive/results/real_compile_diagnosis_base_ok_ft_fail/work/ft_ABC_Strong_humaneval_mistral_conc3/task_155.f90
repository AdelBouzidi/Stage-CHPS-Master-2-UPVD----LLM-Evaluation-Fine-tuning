program even_odd_count
  implicit none
  integer :: num
  integer :: even_count, odd_count
  character(len=1) :: digit
  integer :: i

  ! Read input from stdin
  read(*,*) num

  ! Initialize counters
  even_count = 0
  odd_count = 0

  ! Convert number to string and count even/odd digits
  write(0,'(I0)') num
  read(0,'(A)') digit
  do i = 1, len(digit)
    if (i == 1 .and. digit(i:i) == '-') then
      cycle
    end if
    if (mod(int(digit(i:i)), 2) == 0) then
      even_count = even_count + 1
    else
      odd_count = odd_count + 1
    end if
  end do

  ! Output result
  print *, even_count, odd_count

end program even_odd_count