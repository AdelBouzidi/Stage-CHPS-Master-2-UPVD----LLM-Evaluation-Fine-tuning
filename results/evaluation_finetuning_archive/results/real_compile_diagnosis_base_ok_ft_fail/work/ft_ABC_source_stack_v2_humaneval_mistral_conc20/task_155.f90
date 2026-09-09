program even_odd_count_demo
  implicit none
  integer :: num
  integer :: even_count, odd_count
  character(len=1) :: digit
  integer :: i, len
  character(len=20) :: str

  ! Read input number
  read(*,*) num

  ! Initialize counters
  even_count = 0
  odd_count = 0

  ! Convert number to string
  write(str,*) num

  ! Process each digit
  len = len_trim(str)
  do i = 1, len
    digit = str(i:i)
    if (i == 1 .and. digit == '-') then
      cycle
    end if
    if (mod(iachar(digit), 2) == 0) then
      even_count = even_count + 1
    else
      odd_count = odd_count + 1
    end if
  end do

  ! Output result
  print *, even_count, odd_count

end program even_odd_count_demo